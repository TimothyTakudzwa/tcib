from django.contrib.auth.models import User, Group
from rest_framework import serializers

from transaction.models import Transaction


class PaymentSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields= ['sender_name', 'sender_street_name' , 'sender_town_name' ,'sender_account_number', 'reference',
        'receiver_name','receiver_street_name' ,'receiver_town_name' ,'receiver_account_number' ,'spid' ,'participant_id' ,'receiving_agent_participant_id']





