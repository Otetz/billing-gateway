from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist


class Payment(models.Model):

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    @cached_property
    def sender(self):
        return self._get_sender_receiver(settings.CREDIT)

    @cached_property
    def receiver(self):
        return self._get_sender_receiver(settings.DEBIT)

    def _get_sender_receiver(self, direction):
        operation = self.operation_list.get(
            direction=direction,
            kind=settings.TRANSFER,
        )
        return operation.account.user

    @cached_property
    def fee(self):
        try:
            return self.operation_list.get(
                direction=settings.CREDIT,
                kind=settings.FEE,
            ).amount
        except ObjectDoesNotExist:
            return Decimal('0')

    @cached_property
    def amount(self):
        operation = self.operation_list.get(
            direction=settings.CREDIT,
            kind=settings.TRANSFER,
        )
        return operation.amount