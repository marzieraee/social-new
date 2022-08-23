import datetime
import jwt 

from django.conf import settings
key='yesss'

def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
        'username':user.username
    }
    access_token = jwt.encode(payload=access_token_payload,key=settings.SECRET_KEY, algorithm='HS256')
    
    
    print(access_token,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        payload=refresh_token_payload, key=settings.SECRET_KEY, algorithm='HS256')

    return refresh_token