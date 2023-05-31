from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now

class Transaction(models.Model):
    tr_id = models.CharField(max_length=100)
    from_address = models.CharField(max_length=100)
    to_address = models.CharField(max_length=100)
    fee = models.CharField(max_length=100)
    gas_price = models.CharField(max_length=100)
    gas_limit = models.CharField(max_length=100)
    gas_used = models.CharField(max_length=100)
    contract_address = models.CharField(max_length=100)
    date = models.IntegerField()
    status = models.CharField(max_length=100)
    tr_type = models.CharField(max_length=100)
    block = models.IntegerField()
    value = models.CharField(max_length=100)
    nonce = models.IntegerField()
    native_token_decimals = models.IntegerField()
    description = models.CharField(max_length=100)
    received = models.JSONField(null=True, blank=True)
    sent = models.JSONField(null=True, blank=True)
    others = models.JSONField(null=True, blank=True)
    input_data = models.CharField(max_length=100)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.tr_id
