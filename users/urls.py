from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, FriendList, PersonList, \
    MessageListCreateView, MessageInBoxListCreateView, VideoAddView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/friend/', FriendList.as_view(), name='friend'),
    path('accounts/friend/<int:person_id>/', FriendList.as_view(), name='friend-list'),
    path('accounts/person/', PersonList.as_view(), name='person-list'),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/inbox/', MessageInBoxListCreateView.as_view(), name='message-in-box-list-create'),
    path('video/add/', VideoAddView.as_view(), name='video-add'),
    path('videos/get/', VideoAddView.as_view(), name='videos-get'),
    # path('message/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-retrieve-update-destroy'),

]