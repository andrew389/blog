from django.views import View
from django.shortcuts import render, redirect
from .models import News
from .utils import fetch_and_save_news


class NewsListView(View):
    @staticmethod
    def get(request):
        news = News.objects.all().order_by('-created_at')
        return render(request, 'news/news_list.html', {'news': news})


class FetchNewsView(View):
    @staticmethod
    def post(request):
        fetch_and_save_news()
        return redirect('news_list')
