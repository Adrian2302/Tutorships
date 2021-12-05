from django.views.generic import View
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Chat.models import Room, Message


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
