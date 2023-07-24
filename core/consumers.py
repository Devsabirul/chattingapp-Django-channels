from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Websocket connect.")
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs'].get('id')
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def receive(self,text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        receiver = data['receiver_username']
        

        await self.save_message(sender_id,self.room_group_name,message,receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id':sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

        
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )
        print("Websocket disconnect.")

    @database_sync_to_async
    def save_message(self,send_by_id,thread_name,message,recevier):
        chat_obj = Chat.objects.create(sender=send_by_id,thread_name=thread_name,message=message)
        other_user_id = self.scope['url_route']['kwargs']['id']
        get_user  = User.objects.get(id=other_user_id)
        if recevier == get_user.username:
            ChatNotification.objects.create(chat=chat_obj,user=get_user)



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Websocket connect..")
        my_id = self.scope['user'].id
        self.room_group_name = f'{my_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self,text_data=None,bytes_data=None):
        print("msg receive")


    async def send_notificatino(self,event):
        data = json.loads(event.get('value'))
        count = data['count']
        await self.send(text_data=json.dumps({
            'count':count
        }))

    async def disconnect(self,code):
        print('Websocket disconnect..')