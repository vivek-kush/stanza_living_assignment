from django.db.models.fields.json import JSONField
from django.db import models


class Ledger(models.Model):
    
    reference_id = models.CharField(max_length=50)
    reference_type = models.CharField(max_length=50)
    ledger_type = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
    debit = models.DecimalField(max_digits=20, decimal_places=2)
    credit = models.DecimalField(max_digits=20, decimal_places=2)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    metadata = JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
