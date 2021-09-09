import datetime
import jwt
from django.conf import settings
from wallet.models import WalletUser

def generate_access_token(object):
    payload = {
        'user': object,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, "HS256")

    return access_token


def jwt_decode(request):
    authorization_heaader = request.headers.get('Authorization')
    access_token = authorization_heaader.split(' ')[1]
    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=['HS256'])

    id = payload['user']['customer_xid']
    user = WalletUser.objects.get(customer_xid=id)
    return user