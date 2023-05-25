from rest_framework import serializers
from django.contrib.auth import password_validation as pv

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'telegram_chat_id', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароль не совпадают')
        for i in attrs['telegram_chat_id']:
            if not i.isdigit():
                raise serializers.ValidationError('В поле можно указывать только цифры')
            return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            telegram_chat_id=validated_data.get('telegram_chat_id'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class StaffRegisterSerializer(UserRegisterSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data.get('username'),
            telegram_chat_id=validated_data.get('telegram_chat_id'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password']),
        user.is_staff = True
        user.save()
        return user


