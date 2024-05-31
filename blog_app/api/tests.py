from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import CustomUser
from articles.models import Article


class ArticleTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', age=25)
        self.owner = CustomUser.objects.create_user(username='owneruser', password='ownerpassword', age=30)

        self.article = Article.objects.create(title='Test Article', body='Test Content', author=self.owner)

        self.list_url = reverse('article_list_api')
        self.create_url = reverse('article_create_api')
        self.detail_url = reverse('article_detail_api', args=[self.article.id])

        self.client = APIClient()

    def test_article_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_create_unauthenticated(self):
        response = self.client.post(self.create_url, {'title': 'New Article', 'body': 'New Content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_create_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.create_url, {'title': 'New Article', 'body': 'New Content'})
        self.assertEqual(response.status_code, 400)

    def test_article_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_update_not_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.put(self.detail_url, {'title': 'Updated Title', 'body': 'Updated Content'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_update_owner(self):
        self.client.login(username='owneruser', password='ownerpassword')
        response = self.client.put(self.detail_url, {'title': 'Updated Title', 'body': 'Updated Content'})
        self.assertEqual(response.status_code, 400)

    def test_article_delete_not_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_delete_owner(self):
        self.client.login(username='owneruser', password='ownerpassword')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
