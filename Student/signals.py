# your_app/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Student

@receiver(pre_delete, sender=Student)
def delete_related_account(sender, instance, **kwargs):
    # Disconnect the signal temporarily to prevent recursion
    pre_delete.disconnect(delete_related_account, sender=Student)

    try:
        if instance.Account_id:
            with transaction.atomic():
                instance.Account_id.delete()
    finally:
        # Reconnect the signal after the deletion
        pre_delete.connect(delete_related_account, sender=Student)