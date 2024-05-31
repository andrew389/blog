from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile/profile_edit.html'
    success_url = reverse_lazy('profile_detail')

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user
