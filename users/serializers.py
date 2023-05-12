from rest_framework import serializers
from .models import MyUser, Friend, ExternalCompany, ExternalContact, Message, Video, Like


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['firstName','lastName','username', 'email', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(firstName=self.validated_data['firstName'], lastName=self.validated_data['lastName'], username=self.validated_data['username'], email=self.validated_data['email'], date_of_birth=self.validated_data['date_of_birth'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class ExternalCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalCompany
        fields = '__all__'

class ExternalContactSerializer(serializers.ModelSerializer):
    external_company = ExternalCompanySerializer()

    class Meta:
        model = ExternalContact
        fields = ('id', 'person', 'external_company')


class PersonSerializer(serializers.ModelSerializer):
    person_ExternalContact = ExternalContactSerializer(many=True)
    number_of_following = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    class Meta:
        model = MyUser
        fields = ('id', 'firstName', 'lastName', 'username', 'email', 'age', 'is_company', 'profile_picture', 'person_ExternalContact', 'number_of_following', 'number_of_followers', 'number_of_likes', 'description')
    def get_number_of_following(self, obj):  # Metoda dostaje pojedynczy obiekt który jest serializowany (prefix get_)
        return obj.person.all().count()
    def get_number_of_followers(self, obj):  # Metoda dostaje pojedynczy obiekt który jest serializowany (prefix get_)
        return obj.person_friends.all().count()
    def get_number_of_likes(self, obj):
        return obj.get_likes_count()

class UpdateFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

class ShowFriendSerializer(serializers.ModelSerializer):
    friend = PersonSerializer()

    class Meta:
        model = Friend
        fields = ('friend',)

class MessageSerializer(serializers.ModelSerializer):
    sender = PersonSerializer(read_only=True)
    receiver = PersonSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'created_at']

class UpdateMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class AddVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideosSerializer(serializers.ModelSerializer):
    user = PersonSerializer(read_only=True)
    number_of_likes = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'

    def get_number_of_likes(self, obj):  # Metoda dostaje pojedynczy obiekt który jest serializowany (prefix get_)
        return obj.liked_video.all().count()
    def get_user_has_liked(self, obj):
        user_id = self.context['user_id']
        return Like.objects.filter(person=user_id, video=obj).exists()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'