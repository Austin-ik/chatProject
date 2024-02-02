import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate the user during connection
        user = self.scope["user"]
        if user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Clean up on disconnection, if needed
        pass

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        # Save the message to the database using the serializer
        serializer = MessageSerializer(data={'sender': sender, 'receiver': receiver, 'content': content})
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @database_sync_to_async
    def get_message(self, message_id):
        # Retrieve the message from the database using the serializer
        try:
            message = Message.objects.get(id=message_id)
            serializer = MessageSerializer(message)
            return serializer.data
        except Message.DoesNotExist:
            return None

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        receiver_username = data['receiver']  # Assuming you send the receiver's username from the frontend

        # Find the receiver User instance
        receiver = await self.get_user_by_username(receiver_username)

        if receiver:
            # Save the message to the database using database_sync_to_async
            message = await self.save_message(self.scope["user"], receiver, message_content)

            # Update read status in the database
            # In a real application, you would likely identify the message and update its read status
            message.read = True
            message.save()

            # Get the serialized message
            serialized_message = await self.get_message(message.id)

            # Send read receipt back to the sender
            await self.send(text_data=json.dumps(serialized_message))
        else:
            # Handle the case where the receiver is not found (e.g., invalid username)
            pass

    @database_sync_to_async
    def get_user_by_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
