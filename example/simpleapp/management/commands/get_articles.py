# -*- coding:utf-8 -*-
"""

"""
import os

from django.core.management.base import BaseCommand
from dateutil import parser as tparser
from bs4 import BeautifulSoup
import feedparser

from simpleapp.models import Article

FEEDS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'urls.txt')


class Command(BaseCommand):
    help = 'Retrieve rss article feeds'

    def handle(self, *args, **options):
        with open(FEEDS) as f:
            urls = f.readlines()
            for url in urls:
                url = url.strip()
                self.get_feed_entries(url)

    def get_feed_entries(self, url):
        parse = feedparser.parse(url)
        num = len(parse.entries)
        if num > 0:
            for entry in parse.entries:
                title = getattr(entry, 'title', None)
                url = getattr(entry, 'link', None)
                desc = getattr(entry, 'description', None)
                image = parse.get('image', '')
                if not desc:
                    desc = getattr(entry, 'summary', None)

                description = BeautifulSoup(desc).get_text()
                item, created = Article.objects.get_or_create(
                    title=title, url=url, desc=desc)

                pubdate = getattr(entry, 'published', None)
                if pubdate:
                    item.created = tparser.parse(pubdate, ignoretz=True)

                udate = getattr(entry, 'updated', None)
                if udate:
                    item.updated = tparser.parse(udate, ignoretz=True)
                item.save()
                print item.title
