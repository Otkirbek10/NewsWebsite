from django.shortcuts import render,get_object_or_404
from .models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def post_list(request):
    posts = Post.published.order_by('-publish')[1:]
    latest = Post.published.order_by('-publish').first()
    return render(request,'blog/list.html',{'posts': posts,'latest':latest})

def post_detail(request,year,month, day, slug):
    post = get_object_or_404(Post, slug = slug,status = Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day)
    return render(request,'blog/detail.html',{'post': post})