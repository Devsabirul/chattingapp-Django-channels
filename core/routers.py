from django.urls import path
from .consumers import *

websocket_urlspatterns = [
    path('notification',NotificationConsumer.as_asgi()),
    path('chats-page/<int:id>',PersonalChatConsumer.as_asgi())
]