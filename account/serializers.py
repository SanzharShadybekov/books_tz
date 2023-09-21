from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True,)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,
                                     write_only=True, required=True)
    password2 = serializers.CharField(min_length=8,
                                      write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Passwords didn\'t match!')
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ConfirmedUserRegisterSerializer(RegisterSerializer):
    def create(self, validated_data):
        user = User.objects.create(is_active=True, **validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
