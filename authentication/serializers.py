from rest_framework import serializers
from django.contrib.auth.models import User
from .mixins import JWTTokenMixin
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_staff', 'full_name', 'is_active')
        read_only_fields = ('is_active', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_full_name(self, obj):
        if obj.first_name and obj.last_name:
            return '{} {}'.format(obj.first_name, obj.last_name)
        return ""


class UserSerializerWithJWT(JWTTokenMixin, UserSerializer):
    token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('token',)


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Email is already exist. Please try another email.")
        ]
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active')


class NewUserSerializer(UserSerializer):
    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="Email is already exist. Please try another email."
        )]
    )

    class Meta(UserSerializer.Meta):

        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_staff', 'is_active')
        extra_kwargs = {}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(NewUserSerializer, self).create(validated_data)
