from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import SignUpView, ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
