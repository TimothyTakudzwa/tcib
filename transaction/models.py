import datetime
from django.db import models

# Create your models here.
class Transaction(models.Model):
    sender_name = models.CharField(max_length=255, null=False, blank=False)
    sender_street_name = models.CharField(max_length=255, null=False, blank=False)
    sender_town_name = models.CharField(max_length=255, null=False, blank=False)
    sender_account_number = models.CharField(max_length=255, null=False, blank=False)
    receiver_name = models.CharField(max_length=255, null=False, blank=False)
    receiver_street_name = models.CharField(max_length=255, null=False, blank=False)
    receiver_town_name = models.CharField(max_length=255, null=False, blank=False)
    receiver_account_number = models.CharField(max_length=255, null=False, blank=False)
    spid = models.CharField(max_length=255, null=False, blank=False)
    participant_id = models.CharField(max_length=255, null=False, blank=False)
    receiving_agent_participant_id = models.CharField(max_length=255, null=False, blank=False)
    reference = models.CharField(max_length=255, null=False, blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    updated_on = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=255, null=False, blank=False)
    is_successful = models.BooleanField(default=False)
    