from django.forms import ModelForm,TextInput, Textarea,FileInput,Select,Form
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django import forms
from captcha.fields import CaptchaField


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','image','body']

        widgets = {
            'photo': FileInput(attrs={
                'class': 'form-control'
            })
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': Textarea(attrs={
                'rows': 3,
                'class': 'form-control' ,
                'placeholder': 'Leave a comment'   

            })
        }

        

class ContactForm(Form):
    name = forms.CharField(label = 'Name', max_length=50)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'cols':60,
            'rows': 10
        }
    ))
    captcha = CaptchaField()


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea,required=False)
    