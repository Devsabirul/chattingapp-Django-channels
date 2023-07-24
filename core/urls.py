from django.urls import path
from .views import *
urlpatterns = [
   path('welcome-page', welcomePage, name="welcomePage"),
   path('', home, name="Home"),
   path('chats', chats, name="chats"),
   path('chats-page/<int:id>', chats_page, name="chats_page"),
   path('calls', calls, name="calls"),
   path('voice-call/<int:id>', voice_call, name="voice_call"),
   path('settings', settings, name="settings"),
]
    