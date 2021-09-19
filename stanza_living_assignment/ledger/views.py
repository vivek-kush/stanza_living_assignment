import json

from multiprocessing import Process

from ledger.models import Ledger
from ledger.helper import Validator, Converter, HealthCheck

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

DEBIT = 'debit'
CREDIT = 'credit'

@api_view(['POST'])
@csrf_exempt
def make_entry(request):
        
    data = Validator.validateJSON(request.body)

    if not data:
        return Response({"status": "error", "data": {'error': 'Invalid request body'}}, status=status.HTTP_400_BAD_REQUEST)
    
    reference_id = data.get('reference_id')
    reference_type = data.get('reference_type')
    ledger_type = data.get('ledger_type')
    unit = data.get('unit')
    debit = data.get('debit') or 0.00
    credit = data.get('credit') or 0.00
    description = data.get('description')
    metadata = data.get('metadata')

    ledger_entries = Ledger.objects.filter(reference_id=reference_id, ledger_type=ledger_type, reference_type=reference_type)
    balance = 0.00
    
    balance = round(float(sum([ledger_entry.debit - ledger_entry.credit for ledger_entry in ledger_entries])), 2)

    balance += debit - credit
    
    new_ledger_entry = Ledger(reference_id=reference_id, reference_type = reference_type, ledger_type=ledger_type, unit=unit, debit=debit, credit=credit, 
    description=description, metadata=metadata, balance=balance)

    new_ledger_entry.save()

    try:
        HealthCheck.health_check(new_ledger_entry)
    except Exception as e:
        print(e)
    
    return Response({"status": "success", "data": {"message": "new ledger successfully added"}}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_ledger(request):

    data = request.GET

    reference_id = data.get('reference_id')
    reference_type = data.get('reference_type')
    ledger_type = data.get('ledger_type')

    if not Validator.required_params(reference_id=reference_id, reference_type=reference_type, ledger_type=ledger_type):
        return Response({"status": "error", "data": {'error': 'Required parameters not present'}}, status=status.HTTP_400_BAD_REQUEST)

    ledger_entries = Ledger.objects.filter(reference_id=reference_id, ledger_type=ledger_type).order_by('created_at')

    entries = []

    for ledger_entry in ledger_entries:

        transaction_type = DEBIT if int(ledger_entry.debit) != 0 else CREDIT
        
        entry_data = {
            "transaction_type": transaction_type,
            transaction_type:  ledger_entry.debit if transaction_type == DEBIT else ledger_entry.credit,
            'balance': ledger_entry.balance,
            'metadata': Converter.convert_to_dict(ledger_entry.metadata)
        }

        entries.append(entry_data)


    result = {
        "reference_id": reference_id,
        "reference_type": reference_type,
        "ledger_type": ledger_type,
        "entries": entries
    }

    return Response({"status": "success", "data": result}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_final_balance(request):

    data = request.GET

    reference_id = data.get('reference_id')
    reference_type = data.get('reference_type')
    ledger_type = data.get('ledger_type')

    if not Validator.required_params(reference_id=reference_id, reference_type=reference_type, ledger_type=ledger_type):
        return Response({"status": "error", "data": {'error': 'Required parameters not present'}}, status=status.HTTP_400_BAD_REQUEST)

    ledger_entries = Ledger.objects.filter(reference_id=reference_id, ledger_type=ledger_type).order_by('created_at')

    if not ledger_entries:
        return Response({"status": "error", "data": {'error': 'No entries found'}}, status=status.HTTP_400_BAD_REQUEST)

    last_entry = ledger_entries[0]

    return Response({"status": "success", "data": {'final_balance': round(float(last_entry.balance), 2)}}, status=status.HTTP_200_OK)
