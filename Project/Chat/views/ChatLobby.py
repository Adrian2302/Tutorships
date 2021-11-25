from django.views.generic import View
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Chat.models import Room, Message


class ChatLobby(View):
    template_name = 'home.html'
    user: User = None

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        context = {
            'current_user': user,
        }
        return render(request, self.template_name, context)
