from django.urls import path
from .api_views import blog_create_api, blog_list_api, blog_detail_api, blog_update_api

urlpatterns = [
    path('blogs/', blog_list_api),
    path('blogs/<int:id>/', blog_detail_api),
    path('blogs/<int:id>/update/', blog_update_api, name='blog-update-api'),
    path('blogs/create/', blog_create_api, name='blog-create-api'),
]