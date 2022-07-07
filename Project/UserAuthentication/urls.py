from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
    path('add_administrator', views.add_administrator, name="add_administrator"),
]


