from django.urls import path

from chat.views import RoomDetailAPIView, RoomListAPIView

urlpatterns = [
    path('', RoomListAPIView.as_view(), name='room-list'),
    path('<str:room_name>/', RoomDetailAPIView.as_view(), name='chat-room')
]
