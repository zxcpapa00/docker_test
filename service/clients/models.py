from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=128)
    full_address = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.user} | {self.company_name}'
