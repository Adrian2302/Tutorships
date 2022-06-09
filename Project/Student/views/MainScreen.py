from django.views import generic
from django.shortcuts import render


class MainScreen(generic.View):

    def get(self, request):
        return render(request, 'Student/index.html', {"title_page": "Inicio"})
