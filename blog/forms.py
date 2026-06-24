from django.forms import ModelForm,TextInput, Textarea,FileInput,Select
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm


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

        