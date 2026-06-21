from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import AddPostForm


def post_list(request):
    posts = Post.published.order_by('-publish')[1:]
    latest = Post.published.order_by('-publish').first()
    paginator = Paginator(posts,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/list.html',{'posts': posts,'latest':latest})

def post_detail(request,year,month, day, slug):
    post = get_object_or_404(Post, slug = slug,status = Post.Status.PUBLISHED, publish__year = year, publish__month = month, publish__day = day)
    return render(request,'blog/detail.html',{'post': post})

def add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        print(request.POST)
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid(): 
            post = form.save(commit=False) # 2. Holds the save process
            post.author = request.user     # 3. Automatically injects the logged-in user
            post.save()                    # 4. Safely saves to database
            return redirect('/')
        else:
            print("Form Errors:", form.errors) 
    else:
        form = AddPostForm()
    return render(request,'blog/addpost.html', context={'form': form})


def edit_post(request,post_id):
    post = Post.objects.get(pk = post_id)
    form = AddPostForm(instance=post)

    if request.method == "POST":
        form = AddPostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    return render(request,'blog/editpost.html', {'form': form}) 

def delete_post(request,post_id):
    post = Post.objects.get(pk = post_id)
    if request.user != post.author:
        return HttpResponse("You can't delete this post")
    else:
        post.delete()
        return redirect('/')
        