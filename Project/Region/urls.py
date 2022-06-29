from django.urls import path
from . import views

urlpatterns = [
    path('add_region', views.AddRegion.as_view(), name="add_region"),
    path('edit_region', views.EditRegion.as_view(), name='edit_region'),
    path('edit_region/<int:region_id>', views.EditRegion.as_view(), name='edit_region')
]