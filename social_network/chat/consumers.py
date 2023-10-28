# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#         await self.send(text_data=json.dumps({
#             'type': 'connection established',
#             'message': 'You are now connected'
#         }))


from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from . models import ChatModel
from django.contrib.auth.models import User
from users.models import Profile



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = f'chat_{self.room_name}'  

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            
        )
        await self.accept()
        # await self.send(text_data=self.room_group_name)   

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get('initial_message'):
            username = data['username']
            receiver = data['receiver']

            await self.set_read_status(self.room_group_name, username, receiver)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'is_seen',
                    'receiver': receiver,
                    'username': username,
                }
            )
        else:
            message = data['message']
            username = data['username']
            receiver = data['receiver']

            await self.save_message(username, self.room_group_name, message,receiver)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def is_seen(self, event):
        receiver = event['receiver']
        username = event['username']

        await self.send(text_data=json.dumps({
            'initial' : True,
            'receiver': receiver,
            'username': username,
        }))

    # async def is_seen(self, event):


    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message, receiver):
        receiver_user = User.objects.get(username=receiver)
        chat_obj = ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name, receiver=receiver_user)

        receiver_profile = Profile.objects.get(username=receiver)
        if receiver_profile.online_status:
            chat_queryset = ChatModel.objects.filter(thread_name=thread_name).exclude(sender=username,is_seen=True)
            for chat in chat_queryset:
                chat.is_seen = True
                chat.read_status = True
                chat.save()
        # other_user_id = self.scope['url_route']['kwargs']['id']
        # get_user = User.objects.get(id=other_user_id)
        # if receiver == get_user.username:
        #     ChatNotification.objects.create(chat=chat_obj, user=get_user)

    @database_sync_to_async
    def set_read_status(self, thread_name, username, receiver):
        # Update read_status for messages in the chat thread excluding the current user's messages

        chat_queryset = ChatModel.objects.filter(thread_name=thread_name).exclude(sender=username)
        for chat in chat_queryset:
            chat.is_seen = True
            chat.read_status = True
            chat.save()




class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = User.objects.get(username=username)
        userprofile = Profile.objects.get(user=user)
        if c_type == 'open':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()












    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )


#     # async def receive(self, text_data):
#     #     text_data_json = json.loads(text_data)
#     #     message = text_data_json['message']

#     #     await self.send(text_data=json.dumps({
#     #         'message': message
#     #     }))