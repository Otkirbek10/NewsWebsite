from django.forms import ModelForm,TextInput, Textarea,FileInput,Select
from .models import Post
from django.contrib.auth.forms import UserCreationForm


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','image', 'body']

        widgets = {
            'photo': FileInput(attrs={
                'class': 'form-control'
            })
        }


        