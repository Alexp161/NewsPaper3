from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import Post, Category, Comment
from .forms import ContactForm, SubscriptionForm
from django.db import models
from .forms import ArticleForm
from .models import Article
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'news/article_detail.html'
    context_object_name = 'article'


class ArticleListView(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    ordering = '-datetime_create'
    paginate_by = 10


class ArticleCreateView(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('article_list')


class ArticleUpdateView(UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'news/article_update.html'
    context_object_name = 'article'
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('article_list')


def signup(request):
    # Ваш код для регистрации пользователя
    pass

class PostListView(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/detail.html'
    context_object_name = 'post'


@method_decorator(permission_required('news.add_post'), name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'news/create.html'
    fields = ['title', 'content', 'categories']
    success_url = reverse_lazy('index')


@method_decorator(permission_required('news.change_post'), name='dispatch')
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/edit.html'
    fields = ['title', 'content', 'categories']
    context_object_name = 'post'
    success_url = reverse_lazy('index')


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news/index.html', {'posts': posts})


def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'news/detail.html', {'post': post})


def author_request(request):
    authors = User.objects.filter(groups__name='Authors')
    return render(request, 'news/authors.html', {'authors': authors})


def subscribe_categories(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SubscriptionForm()
    return render(request, 'news/subscribe.html', {'form': form})

class Group(models.Model):
    name = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

def send_article_notification(article):
    subscribers = article.category.subscribers.all()
    subject = f'Новая статья в категории {article.category}'
    message = render_to_string('email/article_notification.html', {'article': article})
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, 'from@example.com', [user.email for user in subscribers], html_message=message)

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            send_article_notification(article)  # Отправка уведомления
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

def unsubscribe(request):
    if request.method == 'POST':
        request.user.subscribed_categories.clear()
        return redirect('profile')  # Перенаправление на страницу профиля пользователя
    return render(request, 'unsubscribe.html')
