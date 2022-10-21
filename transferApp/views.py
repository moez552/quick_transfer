from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

from .serializers import HistorySerializer,ProfileSerializer,UserSerializer,CreateUserSerializer
from .models import History
from rest_framework.permissions import IsAuthenticated

from transferApp import serializers

class HistoryView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return History.objects.filter(profile=profile)
    def get_serializer_context(self):
        return {'request': self.request}
    serializer_class  = HistorySerializer

class UsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return User.objects.exclude(id=user.id).filter(is_staff=False)
    serializer_class  = UserSerializer
class ProfileView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user.id)
    serializer_class  = ProfileSerializer
class RegisterView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer



