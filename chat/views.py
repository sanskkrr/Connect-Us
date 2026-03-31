from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message


@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    # ✅ GET BOTH SIDES MESSAGES
    messages = Message.objects.filter(
        sender=request.user, receiver=other_user
    ) | Message.objects.filter(
        sender=other_user, receiver=request.user
    )

    # ✅ IMPORTANT: ORDER THEM
    messages = messages.order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_user': other_user
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def messages_list(request):
    following = request.user.profile.following.all()

    return render(request, 'chat/messages.html', {
        'following': following
    })