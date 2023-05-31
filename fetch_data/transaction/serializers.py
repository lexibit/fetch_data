from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  
    # def __init__(self, *args, **kwargs):
    #     fields = kwargs.pop('fields', None)
    #     super(TransactionSerializer, self).__init__(*args, **kwargs)
    #     if fields is not None:
    #         allowed = set(fields)
    #         existing = set(self.fields)
    #         for field_name in existing - allowed:
    #             self.fields.pop(field_name)