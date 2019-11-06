
import jwt
from rest_framework_jwt.settings import api_settings


def decode(token):
    print(api_settings.JWT_SECRET_KEY)
    print(token.decode('utf-8'))
    user = jwt.decode(token.decode('utf-8'),api_settings.JWT_SECRET_KEY,api_settings.JWT_VERIFY, algorithms=[api_settings.JWT_ALGORITHM])
    return user



