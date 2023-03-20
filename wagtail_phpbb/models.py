from django.db import models
from home.normal_page import NormalPage
from django.conf import settings
import random
import pymysql.cursors

class ForumSearchPage(NormalPage):
  def get_context(self, request, *args, **kwargs):
    context = super().get_context(request, *args, **kwargs)
    filter = {}
    sort = request.GET.get('sort', random.randint(0, 1000))
    filter['sort'] = sort

    skip = int(request.GET.get('skip', 0))
    page_size = 50

    author = request.GET.get('author', None)
    forum = request.GET.get('forum', None)
    if author:
      filter['author'] = int(author)
    if forum:
      filter['forum'] = int(forum)

    forum_db = settings.FORUM_DATABASE
    forum_db = {k.lower(): v for k, v in forum_db.items()}
    del forum_db['name']
    del forum_db['conn_max_age']
    del forum_db['conn_health_checks']
    del forum_db['engine']
    forum_db['database'] = forum_db['user']
    connection = pymysql.connect(**forum_db)

    with connection:
      with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        params = ()
        sql = """
SELECT
  t.topic_id,
  u.username,
  u.user_id,
  t.topic_title,
  from_unixtime(t.topic_time) AS topic_time,
  t.topic_replies,
  pt.post_text,
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

    return context
