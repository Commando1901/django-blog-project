from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('logout_confirm/', views.logout_confirm, name='logout_confirm'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path("blog/<int:id>/", views.blog_detail, name="blog_detail"),
    path("edit/<int:id>/", views.edit_blog, name="edit_blog"),
    path("delete/<int:id>/", views.delete_blog, name="delete_blog"),
    path('like/<int:post_id>/', views.like_blog, name='like_blog')
   
]