

from django import forms
from captcha.fields import CaptchaField
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'date', 'content']

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()
