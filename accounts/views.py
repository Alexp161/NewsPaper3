from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import   UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'  # пример имени шаблона
    success_url = reverse_lazy('home') 

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  # пример имени шаблона
