from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Friend, MyUser
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, ShowFriendSerializer, UpdateFriendSerializer, \
    PersonSerializer


# Create your views here.


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST.get('email')
        print('Email:', email)
        password = request.POST.get('password')
        print('password:', password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', 'username': user.username, 'localId': user.id, 'expiresIn': timedelta(minutes=30), **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PersonList(APIView):
    def get(self, request):
        person = MyUser.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)

class FriendList(APIView):
    """
    List all friend, or add a new friend.
    """
    def delete(self, request, *args, **kwargs):
        try:
            person = request.data['person']
            friend = request.data['friend']
            friend_obj = Friend.objects.get(person=person, friend=friend)
            friend_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request, person_id):
        try:
            person = MyUser.objects.get(pk=person_id)
            friend = Friend.objects.filter(person=person)
        except MyUser.DoesNotExist:
            return Response(status=404)

        serializer = ShowFriendSerializer(friend, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UpdateFriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)