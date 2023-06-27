from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .filters import censor
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Category
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Types(models.TextChoices):
        ARTICLE = 'статья', 'статья'
        NEWS = 'новость', 'новость'

    type = models.CharField(max_length=7, choices=Types.choices, default=Types.ARTICLE)
    datetime_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:50] + '...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Comment(models.Model):
    text = models.TextField()
    datetime_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(sum=Sum('rating'))['sum']
        authors_comments_rating = Comment.objects.filter(user=self.user).aggregate(sum=Sum('rating'))['sum']
        comments_rating_from_authors_posts = Comment.objects.filter(post__author=self).aggregate(sum=Sum('rating'))['sum']
        self.rating = posts_rating * 3 + authors_comments_rating + comments_rating_from_authors_posts
        self.save()

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def save(self, *args, **kwargs):
        self.title = censor(self.title)
        self.content = censor(self.content)
        super().save(*args, **kwargs)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'rating', 'author', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating', 'post', 'user']


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


Group.objects.get_or_create(name='common')
Group.objects.get_or_create(name='authors')

# Получим объекты типов содержимого (content types) для модели Post
post_content_type = ContentType.objects.get_for_model(Post)

# Получим необходимые разрешения
create_permission = Permission.objects.get(
    codename='add_post',
    content_type=post_content_type,
)
edit_permission = Permission.objects.get(
    codename='change_post',
    content_type=post_content_type,
)

# Получим группу "authors"
authors_group, _ = Group.objects.get_or_create(name='authors')

# Установим разрешения для группы "authors"
authors_group.permissions.add(create_permission)
authors_group.permissions.add(edit_permission)


def send_article_notification(article):
    subscribers = article.category.subscribers.all()
    subject = f'Новая статья в категории {article.category}'
    message = render_to_string('email/article_notification.html', {'article': article})
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, 'from@example.com', [user.email for user in subscribers], html_message=message)

class User(AbstractUser):
    subscribed_categories = models.ManyToManyField(Category, related_name='subscribers')

    class Meta:
        permissions = [
            ('add_post', 'Can add post'),
            ('change_post', 'Can change post'),
        ]
