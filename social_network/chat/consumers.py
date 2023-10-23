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

        self.room_group_name = f'chat_{self.room_name}'  # Use the correct format for f-strings

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            
        )
        await self.accept()
        # await self.send(text_data=self.room_group_name)   

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        # receiver = data['receiver']

        await self.save_message(username, self.room_group_name, message)
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

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        chat_obj = ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name)
        # other_user_id = self.scope['url_route']['kwargs']['id']
        # get_user = User.objects.get(id=other_user_id)
        # if receiver == get_user.username:
        #     ChatNotification.objects.create(chat=chat_obj, user=get_user)





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
        print(connection_type)
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