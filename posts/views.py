from django.shortcuts import render
from .models import Post
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required


#view for creating a new post

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data = request.POST,files = request.FILES)
        if form.is_valid():
            new_item = form.save(commit = False)
            new_item.user = request.user
            new_item.save()
    else:
        form = PostCreateForm(data = request.GET)

    return render(request , 'posts/create.html',{'form':form})


#view for displaying all posts of the all the users (feed)

def feed(request):
    posts = Post.objects.all()
    return render(request , 'posts/feed.html', {'posts':posts})