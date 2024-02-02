from django.shortcuts import render
from rest_framework.response import Response
from .serializers import MessageSerializer, RoomSerializer
from .models import Room, Message
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404, render


class RoomListAPIView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetailAPIView(APIView):
    def get(self, request, room_name):
        chat_room = get_object_or_404(Room, name=room_name)
        serializer = RoomSerializer(chat_room)
        return Response(serializer.data)
