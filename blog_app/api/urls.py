from django.urls import path
from .views import ArticleListAPIView, ArticleCreateAPIView, ArticleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('v1/articles/', ArticleListAPIView.as_view(), name='article_list_api'),
    path('v1/articles/create/', ArticleCreateAPIView.as_view(), name='article_create_api'),
    path('v1/articles/<int:pk>/', ArticleRetrieveUpdateDestroyAPIView.as_view(), name='article_detail_api'),
]
