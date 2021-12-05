from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import get_template

from UserAuthentication.models import User
from Chat.models import Room, Message
import json


class ChatLobby(View):
    template_name = 'chatLobby.html'
    user: User = None

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        rooms = list(Room.objects.filter(original_user_sender=user) | Room.objects.filter(original_user_receiver=user))

        context = {
            'current_user': user,
            'rooms': rooms,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.is_ajax():
            user = User.objects.get(pk=request.user.id)
            # print(request.POST['room_id'])

            if request.POST.get('room_id'):
                room = Room.objects.get(pk=request.POST['room_id'])
                messages = list(Message.objects.filter(room=room))

                reciever = room.context_reciever(user)
                context = {'messages': messages,
                           'receiver': reciever}
                return HttpResponse(render(request, 'messages.html', context))

            return HttpResponse(render(request, 'messages.html'))
