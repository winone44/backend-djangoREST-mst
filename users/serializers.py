from rest_framework import serializers
from .models import MyUser, Friend, ExternalCompany, ExternalContact


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(username=self.validated_data['username'], email=self.validated_data['email'], date_of_birth=self.validated_data['date_of_birth'])
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
    class Meta:
        model = MyUser
        fields = ('id', 'firstName', 'lastName', 'email', 'age', 'is_company', 'profile_picture', 'person_ExternalContact')


class UpdateFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

class ShowFriendSerializer(serializers.ModelSerializer):
    friend = PersonSerializer()

    class Meta:
        model = Friend
        fields = ('friend',)