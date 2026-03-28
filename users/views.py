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




#USER LOGIN VIEW

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username = data['username'],password = data['password'])
            if user is not None : 
                login(request,user)
                return HttpResponse("User authenticated and LoggedIn")
            else:
                return HttpResponse("Invalid Credentials")

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


#INDEX VIEW 

@login_required 
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user = current_user)
    return render (request , 'users/index.html', {'posts': posts})


#USER REGISTRATION VIEW

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user) #creating profile for new user directly after registration
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form})

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
    profile = request.user.profile

    if target_user.profile in profile.following.all():
        profile.following.remove(target_user.profile)
    else:
        profile.following.add(target_user.profile)

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