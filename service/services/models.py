from django.core.validators import MaxValueValidator
from django.db import models
from .tasks import set_price

from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=128)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):

        if self.full_price != self.__full_price:
            for sub in self.subscriptions.all():
                set_price.delay(sub.id)

        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=20)
    discount_percent = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(100)
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):

        if self.discount_percent != self.__discount_percent:
            for sub in self.subscriptions.all():
                set_price.delay(sub.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.plan_type} - {self.discount_percent}%'


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.client} - {self.service} - {self.plan}'
