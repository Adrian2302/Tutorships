# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('mensajes/', views.ChatLobby.as_view(), name='chatlobby'),
    path('mensajes/<int:user_receiver_pk>', views.ChatRoom.as_view(), name='chatroom'),
    path('mensajes/<int:room_pk>/<int:user_receiver_pk>', views.ChatRoom.as_view(), name='chatroom'),
]
