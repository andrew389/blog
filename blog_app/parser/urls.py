from django.urls import path
from .views import NewsListView, FetchNewsView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('fetch-news/', FetchNewsView.as_view(), name='fetch_news'),
]
