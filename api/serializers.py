from django.contrib.auth.models import User, Group
from rest_framework import serializers

from transaction.models import Transaction

class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, label='currency_code', max_length=255)
    account_number = serializers.CharField(required=True, label='account_number', max_length=255)
    street_name = serializers.CharField(required=True, label='street_name', max_length=255)
    town_name = serializers.CharField(required=True, label='town_name', max_length=255)
    country = serializers.CharField(required=True, label='country', max_length=255)
    postal_code = serializers.CharField(required=True, label='postal_code', max_length=255)
class AmountSerializer(serializers.Serializer):
    amount = serializers.FloatField(required=True, label='amount')
    currency_code = serializers.CharField(required=True, label='currency_code', max_length=255)

    def create(self, validated_data):
        return AmountSerializer(**validated_data)
class PaymentSerializer(serializers.Serializer):
    amount = AmountSerializer(required=True, label='amount')
    sender = CustomerSerializer(required=True, label='sender')
    receiver = CustomerSerializer(required=True, label='receiver')
    purpose = serializers.CharField(required=True)
    participant_id = serializers.CharField(required=True)
    receiving_agent_participant_id = serializers.CharField(required=True)

    class Meta:
        model = Transaction
        fields = ['sender_name', 'sender_street_name', 'sender_town_name', 'sender_account_number',
                  'reference', 'receiver_name', 'receiver_street_name', 'receiver_town_name',
                  'receiver_account_number', 'spid', 'participant_id', 'receiving_agent_participant_id']


