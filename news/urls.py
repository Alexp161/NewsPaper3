


from .views import ArticleDetailView
from django.urls import path
from django.urls import include
from .views import ArticleListView
from .views import ContactView
from django.contrib.auth.views import LoginView
from .views import ArticleCreateView
from .views import signup
from . import views
from django.urls import path
from .views import author_request
from django.urls import path
from .views import unsubscribe
from .views import ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('signup/', signup, name='signup'),
    path('<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('add_article/', ArticleCreateView.as_view(), name='add_article'),
    path('news/search', views.search, name='search'),
    path('author-request/', author_request, name='author_request'),
    path('accounts/', include('allauth.urls')),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='update_article'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete_article'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]
