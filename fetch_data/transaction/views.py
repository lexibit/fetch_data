import requests
import json

from django.shortcuts import render

from .models import Transaction
from .serializers import TransactionSerializer

from balance.models import Balance
from django.db.models import Q
from django.db.models import Max

from rest_framework import generics

from authentication.jwt_utils import *

from django.views.decorators.csrf import csrf_exempt
from authentication.views import *

from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view

api_key = "uzHeGHWaQZFy6cabl7ge1JoueHgTtYZ5CmUiWc60"

@api_view(['GET', 'POST'])
def fetch_data(request):
    if request.method == 'GET':
        chain = request.GET.get('chain')
        address = request.GET.get('address')
    elif request.method == 'POST':
        chain = request.data.get('chain')
        address = request.data.get('address')
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not chain or not address:
        return Response({'error': 'Missing chain or address parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    latest_timestamp = Transaction.objects.filter().aggregate(Max('date_created'))['date_created__max']
    print(latest_timestamp)
    
    url = f"https://api.unmarshal.com/v2/{chain}/token/{address}/transactions"

    if latest_timestamp:
        url += f"?after={latest_timestamp}"

    query = {
        "page": "10",
        "pageSize": "5",
        "before": "string",
        "until": "string",
        "auth_key": api_key
    }

    response = requests.get(url, params=query)

    data = response.json()
    transactions = data.get("transactions", [])
    print(json.dumps(transactions, indent=4))
    
    if response.status_code == 200:
        content = data.get('transactions', '')
        for item in content:
            tr_type = item.get("type")
            print("*******")
            print()
            print(tr_type)
            print("******")
            balance = 0.0
            received = item.get("received", [])
            for receive_item in received:
                for key, value in receive_item.items():
                    if tr_type == "receive" or tr_type == "RECEIVE":
                        if key == "value":
                            balance += float(value)
                    elif tr_type == "send" or tr_type == "send":
                        if key == "value":
                            balance -= float(value)
                            try:
                                Balance.objects.get(address=address)
                                Balance.objects.update(balance=balance)
                            except:
                                Balance.objects.create(balance=balance, address=address)

                    print(f"{key}: {value}")
                print("---")
                
        data = data["transactions"]
        save_transaction(data)
        
        return render(request, 'api/fetch_success.html')
    else:
        return render(request, 'api/fetch_error.html')

    
# def calculate_balance(self):
#             transactions = Transaction.objects.all()
#             print("*********")
#             print(transactions)
#             print("*********")
#             balance = 0.0
#             for transaction in transactions:
#                 if transaction["type"] == "RECEIVE" or transaction["type"] == "receive":
#                     received_data = self.received 
                    
#                     for item in received_data:
#                         value = float(item.get("value", 0))
#                         balance += value
                        
#                 elif transaction.get("type") in ["SEND", "send"]:
#                     sent_data = self.sent  
                
#                     for item in sent_data:
#                         value = float(item.get("value", 0))
#                         balance -= value
            
        
#             Balance.objects.create(balance=balance, address=address)

def save_transaction(data):
   for item in data:
            transaction = Transaction(
                tr_id=item['id'],
                from_address=item['from'],
                to_address=item['to'],
                fee=item['fee'],
                gas_price=item['gas_price'],
                gas_limit=item['gas_limit'],
                gas_used=item['gas_used'],
                contract_address=item['contract_address'],
                date=item['date'],
                status=item['status'],
                tr_type=item['type'],
                block=item['block'],
                value=item['value'],
                nonce=item['nonce'],
                native_token_decimals=item['native_token_decimals'],
                description=item['description'],
                received=item['received'] if 'received' in item else None,
                sent=item.get('sent', []),
                others=item.get('others', []),
                input_data=item['input_data']
            )
            transaction.save() 
           

from django.http import JsonResponse
from rest_framework import status

def jwt_authentication_required(view_func):
    def wrapper(view, *args, **kwargs):
        request = view.request
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        if not token:
            # ne radi u browser-u
            return JsonResponse({'error': 'Authorization required'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = decode_jwt_token(token)
        if not payload:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = payload.get('user_id')
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user = user

        return view_func(view, *args, **kwargs)

    return wrapper


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    @jwt_authentication_required
    def get_queryset(self):
        return Transaction.objects.all()

    @jwt_authentication_required
    def create(self, request, *args, **kwargs):
        payload = request.data
        print("sdnjknwd")
        print(payload)
        print("dwnejkdm")
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        return Response({"id": response.id}, status=status.HTTP_201_CREATED)
