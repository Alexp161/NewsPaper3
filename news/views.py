


from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Article
from django.views.generic.edit import FormView
from .forms import ContactForm
from django.views.generic.edit import CreateView
from .forms import ArticleForm

class ArticleCreateView(CreateView):
    form_class = ArticleForm
    template_name = 'news/add_article.html'  # пример имени шаблона
    success_url = '/'  # URL для перенаправления после успешного добавления статьи

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'  # пример имени шаблона
    success_url = '/'  # URL для перенаправления после успешной отправки формы

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'  # пример имени шаблона
    ordering = ['-date']  # порядок от более свежих до старых

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'  # пример имени шаблона