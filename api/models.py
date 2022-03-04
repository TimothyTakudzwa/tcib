from django.db import models
from django.contrib.auth.models import AbstractUser
from api.constants import PARTICIPANT_TYPES

from api.managers import UserManager
# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=False,unique=True, choices=PARTICIPANT_TYPES)
    spid = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
    
    def __str__(self):
        return f"{self.name} - {self.spid}"
    
class User(AbstractUser):
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, blank=True, null=True)
    

    
   
    


