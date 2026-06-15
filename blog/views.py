from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse

from .models import *

def post_list(request):
    posts = Post.published.all()
    latest = Post.published.order_by('-publish').first()
    return render(request,'blog/list.html',{'posts': posts,'latest':latest})

def post_detail(request,year,month, day, slug):
    post = get_object_or_404(Post, slug = slug,status = Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day)
    return render(request,'blog/detail.html',{'post': post})