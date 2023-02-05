from django.db import models

from utility.models import BaseModel


class TicketMessage(BaseModel):
    ticket = models.ForeignKey(
        to='crm.Ticket',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='تیکت مربوطه'
    )

    message = models.TextField(
        verbose_name='متن پیام'
    )

    @property
    def try_customer_ticket_message(self):
        if isinstance(self, CustomerTicketMessage):
            return self
        try:
            return self.customerticketmessage
        except:
            return None

    @property
    def try_manager_ticket_message(self):
        if isinstance(self, ManagerTicketMessage):
            return self
        try:
            return self.managerticketmessage
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_customer_ticket_message or self.try_manager_ticket_message

    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'


class CustomerTicketMessage(TicketMessage):

    class Meta:
        verbose_name = 'پیام تیکت مشتری'
        verbose_name_plural = 'پیام‌های تیکت مشتری'


class ManagerTicketMessage(TicketMessage):

    class Meta:
        verbose_name = 'پیام تیکت منیجر'
        verbose_name_plural = 'پیام‌های تیکت منیجر'
