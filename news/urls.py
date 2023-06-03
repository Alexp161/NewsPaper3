


from .views import ArticleDetailView
from django.urls import path
from .views import ArticleListView
from .views import ContactView
from .views import ArticleCreateView
from . import views

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('add_article/', ArticleCreateView.as_view(), name='add_article'),
    path('news/search', views.search, name='search'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='update_article'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete_article'),
]
