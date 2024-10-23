from django.urls import path
from .views import ListCreateGroupView, DeleteGroupView, UpdateGroupView

urlpatterns = [
    path('groups/', ListCreateGroupView.as_view(), name='groups'),
    path('groups/delete/<int:pk>/', DeleteGroupView.as_view(), name='delete_group'),
    path('groups/update/<int:pk>/', UpdateGroupView.as_view(), name='update_group'),
]