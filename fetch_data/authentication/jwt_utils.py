import jwt
from django.conf import settings

def generate_jwt_token(user_id):
    secret_key = 'your_secret_key'
    payload = {'user_id': user_id}
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    
    return token

def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None