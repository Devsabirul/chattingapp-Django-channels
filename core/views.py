from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *
from django.db.models import Q
from django.db.models import Max

def welcomePage(request):
  return render(request,"core/welcome-page.html")


@login_required(login_url='welcomePage')
def home(request):
  users = User.objects.exclude(username=request.user).exclude(is_superuser=True)
  notification_obj = ChatNotification.objects.filter(is_seen=False,user=request.user)
  return render(request,"core/index.html",locals())


@login_required(login_url='welcomePage')
def chats(request):
    users = User.objects.exclude(username=request.user).exclude(is_superuser=True)
    thread = []
    for user in users:
      if request.user.id > user.id:
          thread_name = f'chat_{request.user.id}-{user.id}'
          thread.append(thread_name)
      else:
          thread_name = f'chat_{user.id}-{request.user.id}'
          thread.append(thread_name)
    user_last_messages = []
    for thread_name in thread:
      chat = ChatNotification.objects.filter(chat__thread_name=thread_name).order_by('-id')
      if chat:
        user_last_messages.append(chat[0])
      else:
        user_last_messages.append("You don't have message.")
    unseen_msg = ChatNotification.objects.filter(is_seen=False , user=request.user)

    user_data = zip(users, user_last_messages)
    return render(request, "core/chats.html", locals())



@login_required(login_url='welcomePage')
def chats_page(request,id):
  try:
    user = User.objects.get(id=id)
  except User.DoesNotExist:
    return redirect('chats')

  to_user = User.objects.get(id=id)
  if request.user.id > to_user.id:
      thread_name = f'chat_{request.user.id}-{to_user.id}'
  else:
      thread_name = f'chat_{to_user.id}-{request.user.id}'

  messages = Chat.objects.filter(thread_name=thread_name)

  # is seen false to true ----------------

  unseen_msg = ChatNotification.objects.filter(is_seen=False , user=request.user)
  for i in unseen_msg:
    if i.chat.sender == id:
      i.is_seen = True
      i.save()

   # is seen false to true end ----------------

  return render(request,"core/chats-page.html",locals())



@login_required(login_url='welcomePage')
def calls(request):
  users = User.objects.exclude(username=request.user).exclude(is_superuser=True)
  return render(request,"core/calls.html",locals())


@login_required(login_url='welcomePage')
def voice_call(request,id):
  user = User.objects.get(id=id)
  return render(request,"core/voice-call.html",locals())

@login_required(login_url='welcomePage')
def settings(request):
  user = User.objects.get(username=request.user)
  return render(request,"core/settings.html",locals())

