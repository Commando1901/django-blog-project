from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Blog,Like,Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
        
    return render(request, 'login.html')

def dashboard(request):
    #only show blogs created by logged-in user
    user_posts = Blog.objects.filter(author=request.user)
    return render(request, 'dashboard.html',{"user_posts":user_posts})

@login_required
def home(request):
    all_posts = Blog.objects.all().order_by('-created_at') #newest first
    return render(request, "home.html", {"all_posts":all_posts})


def create_blog(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        #save blog to database
        blog = Blog(author=request.user, title=title, content=content)
        blog.save()

        return redirect('dashboard')
    return render(request, 'create_blog.html')

def blog_detail(request, id):
   
    post = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        comment_text = request.POST.get("comment")

        if comment_text:
            Comment.objects.create(
                blog=post,
                user=request.user,
                text=comment_text
            )

        return redirect("blog_detail", id=post.id)

    comments = post.comments.all().order_by("-created_at")

    return render(request, "blog_detail.html", {
        "post": post,
        "comments": comments,
    })
   
def edit_blog(request, id):
    post = Blog.objects.get(id=id)

    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()
        return redirect("home")

    return render(request, "edit_blog.html", {"post": post})

def delete_blog(request, id):
    post = Blog.objects.get(id=id)
    post.delete()
    return redirect("home")


def logout_confirm(request):
    return render(request, 'logout_confirm.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def like_blog(request, post_id):
    blog = get_object_or_404(Blog, id=post_id)

    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    user_posts = Blog.objects.filter(author=user)

    total_posts = Blog.objects.filter(author=user).count()
    total_likes = Like.objects.filter(user=user).count()
    total_comments = Comment.objects.filter(user=user).count()

    context = {
        'user_obj': user,
        'profile': profile,
        'user_posts': user_posts, 
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }

    return render(request, 'profile.html', context)

def public_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile

    user_posts = Blog.objects.filter(author=user_obj)

    total_posts = user_posts.count()
    total_likes = Like.objects.filter(user=user_obj).count()
    total_comments = Comment.objects.filter(user=user_obj).count()

    context = {
        'user_obj': user_obj,
        'profile': profile,
        'user_posts': user_posts, 
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'is_own_profile': request.user == user_obj
    }

    return render(request, 'profile.html', context)