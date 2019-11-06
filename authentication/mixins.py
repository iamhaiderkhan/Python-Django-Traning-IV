from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class JWTTokenMixin(ModelSerializer):

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


class IsAuthenticateMixin:
    permission_classes = (IsAuthenticated,)

