from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .filters import censor


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Types(models.TextChoices):
        article = 'статья', 'статья'
        news = 'новость', 'новость'

    type = models.CharField(max_length=7, choices=Types.choices, default=Types.article)
    datetime_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

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

    def save(self, *args, **kwargs):
        self.title = censor(self.title)
        self.content = censor(self.content)
        super().save(*args, **kwargs)