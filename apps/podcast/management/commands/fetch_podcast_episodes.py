import feedparser

from time import mktime
from datetime import datetime

from django.core.management.base import BaseCommand

from podcast.models import Podcast, Episode

class Command(BaseCommand):
    args = ''
    help = 'Gets N recent blog posts. Better than parsing the list every page load.'

    def handle(self, *args, **options):
        num_episodes = 3
        
        podcasts = Podcast.objects.all()
        
        for pc in podcasts:

            try:
                feed = feedparser.parse(pc.feed_url)
    
                for ep in pc.episodes.all():
                    ep.delete()
    
                loop_max = num_episodes if len(feed['entries']) > num_episodes else len(feed['entries'])
                
                pc.name = feed['feed'].title if 'title' in feed['feed'] else pc.name
                pc.image = feed['feed'].image.href if 'image' in feed['feed'] else pc.image
                pc.save()
                
                for i in range(0, loop_max):
                    if feed['entries'][i]:
                        e = feed['entries'][i]
                        ep = Episode()
                        ep.podcast = pc
                        ep.title = e.title
                        ep.link = e.link
                        ep.description = e.description
                        ep.date = datetime.fromtimestamp(mktime(e.published_parsed))
                        ep.save()
            except:
                pass # TODO: log the error to the podcast model
