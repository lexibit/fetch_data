from django.http import JsonResponse
from django.contrib.auth import authenticate
from authentication.jwt_utils import generate_jwt_token

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            token = generate_jwt_token(user.id)
            return JsonResponse({'token': token})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)
