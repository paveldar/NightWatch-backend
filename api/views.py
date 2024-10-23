from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User
from .models import Group

import datetime
from .calculations import *


# Create your views here.


# Note Views
class ListCreateGroupView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(creator=user)
    
    def perform_create(self, serializer):

        if serializer.is_valid():
            timeframe = calc_timeframe(self.request.data["time_from"], self.request.data["time_to"])
            num_of_nights = get_night_count(self.request.data["date_from"], self.request.data["date_to"])
            slots_list = calc_slots(self.request.data["participants"], timeframe)
            time_slots = get_time_slots(slots_list, self.request.data["time_from"])
            dates_list = get_dates(self.request.data["date_from"], num_of_nights)
            shifts_list = calc_shifts(dates_list, self.request.data["participants"], time_slots)

            serializer.save(night_count=num_of_nights, duration=timeframe, shifts=shifts_list, creator=self.request.user)
        else:
            print(serializer.errors)


class DeleteGroupView(generics.DestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(creator=user)


class UpdateGroupView(generics.UpdateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(creator=user)



# User Views
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
