from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
import json

# for signals 
from django.db.models.signals import post_save
from django.dispatch import receiver
# for channels 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Chat(models.Model):
    sender = models.PositiveIntegerField(default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class ChatNotification(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.chat.message)


@receiver(post_save,sender=ChatNotification)
def send_notification(sender,instance,created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_obj = ChatNotification.objects.filter(is_seen=False,user=instance.user).count()
        user_id = str(instance.user.id)
        data = {
            'count':notification_obj
        }
        data = json.dumps(data)
        

        async_to_sync(channel_layer.group_send)(
            user_id,
            {
                'type':'send_notificatino',
                'value':data
            }
        )


        print("Send notification")