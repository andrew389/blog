from django.test import TestCase

from .models import News
from .utils import fetch_news, parse_news, fetch_and_save_news


class UtilsTestCase(TestCase):
    def test_fetch_news_success(self):
        html = fetch_news()
        self.assertIsNotNone(html)

    def test_parse_news(self):
        html = fetch_news()
        news_items = parse_news(html)
        self.assertTrue(isinstance(news_items, list))

    def test_parse_news_title_link(self):
        html = fetch_news()
        news_items = parse_news(html)
        for item in news_items:
            self.assertTrue('title' in item)
            self.assertTrue('link' in item)

    def test_parse_news_time_ago(self):
        html = fetch_news()
        news_items = parse_news(html)
        for item in news_items:
            self.assertTrue('time_ago' in item)

    def test_fetch_and_save_news(self):
        fetch_and_save_news()
        news_count = News.objects.count()
        self.assertGreater(news_count, 0)

