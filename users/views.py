from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Friend, MyUser, Message, Video
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer, ShowFriendSerializer, UpdateFriendSerializer, \
    PersonSerializer, MessageSerializer, UpdateMessagesSerializer, AddVideoSerializer, VideosSerializer


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

class PersonInfo(APIView):
    def get(self, request, person_id):
        try:
            person = MyUser.objects.get(pk=person_id)
        except MyUser.DoesNotExist:
            return Response(status=404)
        serializer = PersonSerializer(person)
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

class MessageInBoxListCreateView(APIView):
    serializer_class = MessageSerializer

    def get(self, request):
        receiver = request.query_params.get('receiver')
        queryset = Message.objects.filter(receiver=receiver).order_by('-created_at')[:10]
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
class MessageListCreateView(APIView):
    serializer_class = MessageSerializer

    def get(self, request):
        sender = request.query_params.get('sender')
        receiver = request.query_params.get('receiver')
        queryset = Message.objects.filter(sender=sender, receiver=receiver).order_by('-created_at') | Message.objects.filter(sender=receiver, receiver=sender).order_by('-created_at')
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    # def get(self, request, friend_id):
    #     print('1')
    #     user = 3 #user zalogowany id
    #     print('None')
    #     queryset = Message.objects.filter(sender=3) | Message.objects.filter(receiver=friend_id)
    #     queryset += Message.objects.filter(sender=3) | Message.objects.filter(receiver=3)
    #     serializer = MessageSerializer(queryset, many=True)
    #     return Response(serializer.data)
    def post(self, request):
        serializer = UpdateMessagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MessageRetrieveUpdateDestroyView(APIView):
#     serializer_class = MessageSerializer
#
#     def get_object(self, pk):
#         try:
#             message = Message.objects.get(pk=pk)
#             # Sprawdzenie, czy użytkownik jest nadawcą lub odbiorcą wiadomości
#             print(self.request.user)
#             if message.sender == 11 or message.receiver == 12:
#                 return message
#             else:
#                 return None
#         except Message.DoesNotExist:
#             return None
#
#     def put(self, request, pk):
#         message = self.get_object(pk)
#         if message is not None:
#             serializer = MessageSerializer(message, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, pk):
#         message = self.get_object(pk)
#         if message is not None:
#             message.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)


class VideoAddView(APIView):
    def get(self, request):
        try:
            queryset = Video.objects.all()
            serializer = VideosSerializer(queryset, many=True)
            return Response(serializer.data)
        except MyUser.DoesNotExist:
            return Response(status=404)
    def post(self, request):
        serializer = AddVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)