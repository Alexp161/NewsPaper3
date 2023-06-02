


from .views import ArticleDetailView
from django.urls import path
from .views import ArticleListView
from .views import ContactView
from .views import ArticleCreateView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('add_article/', ArticleCreateView.as_view(), name='add_article'),
]