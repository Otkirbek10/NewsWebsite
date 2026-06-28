from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail

def post_list(request):
    featured_and_posts = list(
    Post.published.select_related('category').order_by('-publish')[:5])
    latest = featured_and_posts[0] if featured_and_posts else None
    posts = featured_and_posts[1:]
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
    related_posts = Post.published.filter(
    category=post.category).exclude(id=post.id)[:3]
    form = CommentForm(request.POST)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post = post).order_by('-created_at').select_related('author')
    return render(request,'blog/detail.html',{'post': post, 'form':form, 'related_posts':related_posts, 'comments': comments})


@login_required(login_url='blog:login')
def add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        print(request.POST)
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.author = request.user     
            post.save()                    
            return redirect('/')
        else:
            print("Form Errors:", form.errors) 
    else:
        form = AddPostForm()
    return render(request,'blog/addpost.html', context={'form': form})

@login_required(login_url='blog:login')
def edit_post(request,post_id):
    post = Post.objects.get(pk = post_id)
    form = AddPostForm(instance=post)

    if request.method == "POST":
        form = AddPostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    return render(request,'blog/editpost.html', {'form': form}) 

@login_required(login_url='blog:login') 
def delete_post(request,post_id):
    post = Post.objects.get(pk = post_id)
    if request.user != post.author:
        return HttpResponse("You can't delete this post")
    else:
        post.delete()
        return redirect('/')
    

def search_post(request):
    query = request.GET.get('query', '').strip()
    page_number = request.GET.get('page', 1)
    if query:
        all_results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
            ).select_related('category')
    else:
        all_results = Post.objects.none() 
    paginator = Paginator(all_results, 3)
    page_obj = paginator.get_page(page_number)

    custom_page_range = paginator.get_elided_page_range(
        number=page_obj.number, 
        on_each_side=2, 
        on_ends=1
    )

    context = {
        'data': page_obj,
        'page_range': custom_page_range,
        'query': query,
    }
    return render(request, 'blog/search.html', context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('blog:login')
            
        return render(request,'blog/register.html',{"form": form})
    

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = name, password = password)

            if user is not None:
                login(request,user)
                return redirect('/')
        return render(request, 'blog/login.html')
 

def logout_user(request):
    logout(request)
    return redirect('/')


def category(request,slug):
    posts = Post.objects.filter(category__slug = slug)
    cat = Category.objects.get(slug = slug)
    return render(request,'blog/category.html',{'posts': posts,'cat':cat})


class ContactView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('/')

    def form_valid(self,form):
        print(form.cleaned_data)
        return redirect('/')
    
def post_share(request,slug):
    post = get_object_or_404(Post, slug = slug,status = Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read ", f"{post.title}"
            message = f"Read {post.title} at {post_url}", f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/share.html',{'post':post,'form':form, 'sent':sent})