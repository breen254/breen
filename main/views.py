from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, userForm, PostForm, CommentForm
from django.contrib import messages
from django.db.models import Q, Count
from .models import Post, Comment, Group, DeliveryRequest
from userAuth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request,None)  
        user = authenticate(request, email = email, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email/Password invalid')
            
    context = {'page':page}
    return render(request, 'main/login-register.html', context)

# ------------------------------------------------LOGOUT------------------------------------------------

def logoutUser(request):
    logout(request)
    return redirect('login')


#-----------------------------------------Register------------------------------------------

def registerUser(request):
    form = MyUserCreationForm()
    
    page = 'register'
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            
            return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')
    else:
        form = MyUserCreationForm()
    
    return render(request, 'main/login-register.html', {'form':form})


# @login_required
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    user = request.user
    posts = Post.objects.filter(availability=True).order_by('-views')
    groups = Group.objects.all()
    post_count = posts.count()
    other_users = User.objects.exclude(id=user.id)
    # post = get_object_or_404(Post)
    # total_favorites = post.favorites.count()
    
    posts = Post.objects.filter(
        Q(group__group__icontains = q)|
        Q(name__icontains = q)|
        Q(price__icontains = q)|
        Q(user__name__icontains = q)|
        Q(content__icontains = q)
        )
    
    context= {
        'posts': posts,
        'post_count':post_count,
        'user':user,
        'groups':groups,
        'other_users':other_users,
        # 'total_favorites':total_favorites,
      
    }
    return render(request,'main/home.html', context)

#-----------------------------------------------------------own profile view--------------------------

@login_required
def edit_profile(request):
    user = User.objects.get(email=request.user)

    if request.method == 'POST':
        form = userForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = userForm(instance=user)

    return render(request, 'main/edit_profile.html', {'form': form})

@login_required
def aboutPage(request):
    page = 'about'
    page = 'contacts'
    return render(request, 'main/about.html')


def delete_post(request, post_id):
    delpost = get_object_or_404(Post, id=post_id)
    if request.user == delpost.user:
        delpost.delete()
    return redirect('user_posts')
        
  

def confirm_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)        
    return render(request, 'main/confirm-delete.html',{'post': post})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        
    return render(request, 'main/create_post.html', {'form': form})  

    
    

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    total_favorites = post.favorites.count()
    
    if request.method == 'POST':
        comment = Comment(
            post=post,
            content=request.POST['content'],
            user=request.user if request.user.is_authenticated else None
        )
        comment.save()
        return redirect('post_detail', post_id=post_id)
    
    # Fetch existing comments for the post
    comments = post.comments.all()
    
    return render(request, 'main/post_detail.html', {'post': post, 'comments': comments, 'total_favorites':total_favorites})
    


def add_to_favorites(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('home')

@login_required
def view_user_posts(request, user_id):
    from django.contrib.auth import get_user_model
    
    User = get_user_model()

    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('home')  # Redirect to home page if the requested user doesn't exist

    posts = Post.objects.filter(user=other_user)

    # Retrieve comments on the other user's posts
    comments = Comment.objects.filter(post__user=other_user)

    return render(request, 'main/view_user_posts.html', {'other_user': other_user, 'posts': posts, 'comments': comments})


@login_required
def user_posts(request):
    comments = Comment.objects.filter(post__user=request.user)
    
    posts = Post.objects.filter(user=request.user)
    post_count = posts.count()
    return render(request, 'main/user_posts.html', {'posts': posts,'comments':comments,'post_count':post_count })

def increment_views(request, post_id):
    product = get_object_or_404(Post, id=product_id)
    product.views += 1
    product.save()
    return redirect('home')

def post_detailed(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_address = request.POST['user_address']
        delivery_request = DeliveryRequest(post=post, user_name=user_name, user_address=user_address)
        delivery_request.save()
        return redirect('home')

    return render(request, 'main/post_detailed.html', {'post': post})

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # Check if the current user is the author of the post
        if request.user == post.user:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('user_posts')
        else:
            return redirect('home')  # Redirect to home if the user is not the author
    else:
        # Check if the current user is the author of the post
        if request.user == post.user:
            form = PostForm(instance=post)
        else:
            return redirect('home')  # Redirect to home if the user is not the author

    return render(request, 'main/update_post.html', {'form': form})