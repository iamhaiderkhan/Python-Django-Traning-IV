from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import authenticate, login
from rest_framework import status
from .serializers import UserSerializer, UserSerializerWithJWT, UserRetrieveUpdateDestroySerializer, NewUserSerializer
from .mixins import IsAuthenticateMixin


# Create your views here.


class LoginView(CreateAPIView):

    serializer_class = UserSerializerWithJWT

    def post(self, request, *args, **kwargs):

        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializerWithJWT(user)
            return Response(serializer.data)
        return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpView(CreateAPIView):
    serializer_class = NewUserSerializer


class UserListView(IsAuthenticateMixin, ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateView(IsAuthenticateMixin, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateDestroySerializer