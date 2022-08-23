import datetime
import jwt
from django.conf import settings


SECRET_KEY='marzie'

def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
        'username':user.username
    }
    access_token1 = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')
    print(access_token_payload,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    
    access_token=access_token1.decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

    return refresh_token




