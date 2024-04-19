from rest_framework import serializers
from api.user.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError("Username and password are required")
        user = User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                User.objects.set_last_login(user)
                return user
            else:
                raise serializers.ValidationError("Password is incorrect")
        else:
            raise serializers.ValidationError("User does not exist")
