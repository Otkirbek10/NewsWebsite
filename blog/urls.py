from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('',post_list,name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',post_detail,name = 'post_detail'),
    path('addpost/', add_post, name = 'add_post'),
    path('edit/<int:post_id>/',edit_post, name = 'edit_post'),
    path("delete/<int:post_id>/",delete_post, name = 'delete'),
    path('search/',search_post,name = 'search'),
    path('register/', register_user, name = 'register'),
    path('login/', login_user, name = 'login'),
    path('logout/', logout_user, name = 'logout')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)