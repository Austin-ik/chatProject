from django.shortcuts import render

# Create your views here.
# chat_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .models import Message
from .serializers import MessageSerializer

@permission_classes([AllowAny])
class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        message_content = request.data.get('message', '')
        sender = request.data.get('sender', '')
        receiver = request.data.get('receiver', '')

        # Save the message to the database using the serializer
        serializer = MessageSerializer(data={'sender': sender, 'receiver': receiver, 'content': message_content})
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        # For simplicity, this example just returns a response with read receipt
        return Response({
            'message': message.content,
            'sender': message.sender,
            'receiver': message.receiver,
            'status': 'delivered',  # Simulating message delivery status
        })
