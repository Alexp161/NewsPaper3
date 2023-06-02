from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory

# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInline,)


admin.site.register(Post, PostAdmin)