

from django import forms
from captcha.fields import CaptchaField
from .models import Article
from .models import News
from .models import Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'date', 'content']

class AuthorRequestForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()

class SubscriptionForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"