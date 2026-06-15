from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('',post_list,name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',post_detail,name = 'post_detail')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)