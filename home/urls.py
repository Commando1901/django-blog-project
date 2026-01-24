from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('like/<int:post_id>/', views.like_blog, name='like_blog'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>', views.public_profile_view, name='public_profile')
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)