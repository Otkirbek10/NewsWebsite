from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=250, db_index= True)
    slug = models.SlugField(max_length=250, db_index= True, unique=True)
    photo = models.ImageField(upload_to="category_photos/%Y/%m/%d/",null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category',args=[self.slug])

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status = Post.Status.PUBLISHED)
        )



class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category,on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/",null=True,blank=True)
    body = RichTextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices= Status, default= Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day,self.slug])



    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args,**kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return "%s - %s" % (self.post.title, self.author.username)