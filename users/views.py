from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate , login
from .forms import LoginForm
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm , ProfileEditForm
from posts.models import Post
from django.contrib.auth.models import User
import requests
import random




#USER LOGIN VIEW

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                login(request, user)
                return redirect("index")   # change if needed
            else:
                form.add_error(None, "Invalid username or password")  # 🔥 KEY LINE

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


#INDEX VIEW 

@login_required
def index(request):
    current_user = request.user

    posts = Post.objects.filter(user=current_user)

    # 🔥 GET PEOPLE YOU FOLLOW
    following_profiles = current_user.profile.following.all()[:5]

    return render(request, 'users/index.html', {
        'posts': posts,
        'following_profiles': following_profiles
    })

#USER REGISTRATION VIEW

def register(request):
    error = None

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # 🔥 IMPORTANT LINE
            user.set_password(form.cleaned_data['password'])

            user.save()
            return redirect("login")
        else:
            error = form.errors

    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {
        "form": form,
        "error": error
    })

#EDIT PROFILE VIEW
@login_required
def edit(request):
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'users/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


#my posts view


@login_required

def my_posts(request):
    user = request.user
    profile = user.profile
    posts = Post.objects.filter(user=user)

    return render(request, 'users/my_posts.html', {
        'posts': posts,
        'profile_user': user,   # ✅ ADD THIS
        'profile': profile      # ✅ ADD THIS
    })


#post detail view
def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'users/post_detail.html', {'post': post})

def intro(request):
    return render(request, 'users/intro.html')

#Follow functionality view

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)

    current_profile = request.user.profile
    target_profile = target_user.profile

    if target_profile in current_profile.following.all():
        current_profile.following.remove(target_profile)
    else:
        current_profile.following.add(target_profile)
    current_profile.save()

    return redirect('profile', username=username)


#Search users view

def search_users(request):
    query = request.GET.get('q')
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, 'users/search.html', {
        'users': users,
        'query': query
    })

#another user profile view


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = user.post_set.all()

    return render(request, 'users/my_posts.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts
    })



#explore view to show posts from API


def search_users(request):
    query = request.GET.get('q')
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    # 🔥 Explore content (random images)
    queries = ["aesthetic", "nature", "travel", "minimal", "city"]
    random_query = random.choice(queries)

    url = f"https://api.pexels.com/v1/search?query={random_query}&per_page=9"

    headers = {
        "Authorization": "bOX4vnEISBWt3982CuUcegPjkGE1z3ri0Ema0elmDim7B0WWq4xaneti"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    images = data.get('photos', [])
    random.shuffle(images)

    return render(request, 'users/search.html', {
        'users': users,
        'query': query,
        'images': images   # 👈 NEW
    })


#following and followers list views

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    profiles = user.profile.following.all()

    return render(request, 'users/user_list.html', {
        'profiles': profiles,
        'title': f"{user.username}'s Following",
        'profile_user': user
    })


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    profiles = user.profile.followers.all()

    return render(request, 'users/user_list.html', {
        'profiles': profiles,
        'title': f"{user.username}'s Followers",
        'profile_user': user
    })