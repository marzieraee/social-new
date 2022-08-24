import datetime
import jwt 

from django.conf import settings


def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=5),
        'iat': datetime.datetime.utcnow(),
        'username':user.username
    }
    access_token1 = jwt.encode(access_token_payload, "secret", algorithm='HS256')
    # access_token=decode('utf-8')
    print(access_token1,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    
    

    return access_token1


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload,settings.SECRET_KEY, algorithm='HS256')

    return refresh_token 