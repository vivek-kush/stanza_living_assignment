import json
import requests
from .models import Ledger

class Validator:
    
    @classmethod
    def validateJSON(cls, jsonData):
        try:
            data = json.loads(jsonData)
        except ValueError as err:
            return None
        return data

    @classmethod
    def required_params(cls, **kwargs):
        for key in kwargs:
            if kwargs[key] is None:
                return False
        return True
    
class Converter:

    @classmethod
    def convert_to_dict(cls, data):
        if data and not isinstance(data, dict):
            try:
                data_dict = json.loads(data)
            except Exception:
                return {}
            return data_dict
        return data

class SlackMessage:

    webhook_url = "https://hooks.slack.com/services/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"

    @classmethod
    def send_message(cls, message):
        payload = {'text': message}
        response = requests.post(cls.webhook_url, data=json.dumps(payload))



class HealthCheck:

    @classmethod
    def health_check(cls, new_ledger_data: Ledger):
        ledger_entries = Ledger.objects.filter(reference_id=new_ledger_data.reference_id, ledger_type=new_ledger_data.ledger_type, 
        reference_type=new_ledger_data.reference_type)
        debits = 0.00
        credits = 0.00

        for ledger_entry in ledger_entries:
            debits += round(ledger_entry.debit)
            credits += round(ledger_entry.credit)

        if new_ledger_data.balance != (debits - credits):
            message = "balance is not matching for reference_id = {}, reference_type = {}, ledger_type = {}".format(
                new_ledger_data.reference_id, new_ledger_data.reference_type, new_ledger_data.ledger_type)
            SlackMessage.send_message(message) 