from django.db import models
from apps.home.normal_page import NormalPage
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from django.conf import settings
import random
import pymysql.cursors

class ForumSearchPage(RoutablePageMixin, NormalPage):
  def get_connection(self):
    forum_db = settings.FORUM_DATABASE
    forum_db = {k.lower(): v for k, v in forum_db.items()}
    forum_db['database'] = forum_db['name']
    del forum_db['name']
    del forum_db['conn_max_age']
    del forum_db['conn_health_checks']
    del forum_db['engine']
    connection = pymysql.connect(**forum_db)
    return connection

  def get_filter(self, request):
    filter = {}

    sort = request.GET.get('sort', random.randint(0, 1000))
    filter['sort'] = sort

    author = request.GET.get('author', None)
    forum = request.GET.get('forum', None)
    scope = request.GET.get('scope', None)
    if author:
      filter['author'] = int(author)
    if forum:
      filter['forum'] = int(forum)
    if scope:
      filter['scope'] = scope

    return filter

  @path('')
  def browse(self, request):
    filter = self.get_filter(request)
    context = {}

    sort = filter['sort']
    skip = int(request.GET.get('skip', 0) or 0)
    scope = request.GET.get('scope', None)
    page_size = 50

    connection = self.get_connection()
    with connection:
      with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        params = ()
        if scope == 'post':
          sql = """
SELECT
  p.post_id,
  t.topic_id,
  u.username,
  u.user_id,
  t.topic_title,
  from_unixtime(t.topic_time) AS topic_time,
  t.topic_replies,
  pt.post_text,
  f.forum_id,
  f.forum_name
  FROM `phpbb_posts` AS p
  INNER JOIN `phpbb_topics` AS t ON t.topic_id = p.topic_id
  INNER JOIN `phpbb_users` AS u ON u.user_id = p.poster_id
  INNER JOIN `phpbb_posts_text` AS pt ON pt.post_id = p.post_id
  INNER JOIN `phpbb_forums` AS f ON f.forum_id = t.forum_id
"""
        else:
          sql = """
SELECT
  t.topic_id,
  u.username,
  u.user_id,
  t.topic_title,
  from_unixtime(t.topic_time) AS topic_time,
  t.topic_replies,
  f.forum_id,
  f.forum_name
  FROM `phpbb_topics` AS t
  INNER JOIN `phpbb_users` AS u ON u.user_id = t.topic_poster
  INNER JOIN `phpbb_posts_text` AS pt ON pt.post_id = t.topic_first_post_id
  INNER JOIN `phpbb_forums` AS f ON f.forum_id = t.forum_id
"""
        if filter:
          sql += "WHERE "
        if 'author' in filter:
          sql += "u.user_id = %s AND "
          params += (filter['author'],)
        if 'forum' in filter:
          sql += "f.forum_id = %s AND "
          params += (filter['forum'],)
        if filter:
          sql += "1 "
        try:
          if sort and int(sort):
            sql += " ORDER BY RAND(%s) "
            params += (sort,)
        except ValueError:
          if sort:
            sql += " ORDER BY "
            if sort == 'topic_time':
              sql += "t.topic_time ASC"
            if sort == 'topic_replies':
              sql += "t.topic_replies DESC"
        sql += """
  LIMIT %s, %s 
"""
        params += (skip, page_size + 1,)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        context['result'] = result

    context['filter'] = filter
    context['page_size'] = page_size
    context['next_skip'] = skip + page_size
    context['prev_skip'] = skip - page_size
    context['skip'] = skip

    return self.render(request, context_overrides=context,
      template='wagtail_phpbb/forum_search_page.html')

  @path('<int:topic_id>/')
  def single_topic(self, request, topic_id):
    context = {}
    connection = self.get_connection()
    with connection:
      with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        params = ()
        params += (topic_id,)
        sql = """
SELECT
  t.topic_id,
  u.username,
  t.topic_title,
  t.topic_first_post_id,
  from_unixtime(t.topic_time) AS topic_time,
  f.forum_id,
  f.forum_name
  FROM `phpbb_topics` AS t
  INNER JOIN `phpbb_users` AS u ON u.user_id = t.topic_poster
  INNER JOIN `phpbb_forums` AS f ON f.forum_id = t.forum_id
  WHERE t.topic_id = %s
"""
        cursor.execute(sql, params)
        result = cursor.fetchone()
        context['topic'] = result

        sql = """
SELECT
  t.topic_title,
  p.post_id,
  u.username,
  u.user_id,
  from_unixtime(p.post_time) AS post_time,
  pt.post_text
  FROM `phpbb_posts` AS p
  INNER JOIN `phpbb_topics` AS t ON t.topic_id = p.topic_id
  INNER JOIN `phpbb_users` AS u ON u.user_id = p.poster_id
  INNER JOIN `phpbb_posts_text` AS pt ON pt.post_id = p.post_id
  WHERE p.topic_id = %s
"""
        cursor.execute(sql, params)
        result = cursor.fetchall()
        context['result'] = result
    return self.render(request, context_overrides=context,
      template='wagtail_phpbb/forum_topic.html')

  def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)
    context['filter'] = self.get_filter(request)
    context['skip'] = int(request.GET.get('skip', 0) or 0)
    return context
