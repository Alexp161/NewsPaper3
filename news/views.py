from django.views.generic import DetailView, ListView, FormView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ContactForm, ArticleForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .forms import AuthorRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

@login_required
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'update_article.html'
    success_url = reverse_lazy('article_list')

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'news/add_article.html'
    success_url = reverse_lazy('article_list')

@method_decorator(permission_required('news.add_post'), name='dispatch')class ContactView(FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'
    success_url = '/'

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    ordering = ['-datetime_create']

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'

def search(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        date = request.POST.get('date')
        # Используйте title, author и date для поиска новостей
        # затем передайте результаты в контекст для отображения в шаблоне
    else:
        # Если метод не POST, отображаем пустую форму
        return render(request, 'search.html', {})

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'update_article.html'
    success_url = reverse_lazy('article_list')

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'delete_article.html'
    success_url = reverse_lazy('article_list')

def post_list_view(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'postList.html', {'page_obj': page_obj})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def author_request(request):
    if request.method == 'POST':
        form = AuthorRequestForm(request.POST)
        if form.is_valid():
            # Получим данные из формы и обработайте их
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # Другие данные из формы

            # Добавим пользователя в группу "authors"
            authors_group = Group.objects.get(name='authors')
            user = User.objects.create_user(username, email=email)
            user.groups.add(authors_group)

            # Дополнительные действия или перенаправление на другую страницу

    else:
        form = AuthorRequestForm()

    return render(request, 'author_request.html', {'form': form})