from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals
from .models import LogEntry

def create_log(user, action, inventory=None, purchase=None, servicing=None, rental=None, disposal=None, note=None):
    LogEntry.objects.create(
        user=user,
        action=action,
        inventory_item=inventory,
        purchase_item=purchase,
        servicing_item=servicing,
        rental_item=rental,
        disposal_item=disposal,
        note=note
    )

# Inventory signals
@receiver(post_save, sender=Inventory)
def log_inventory_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_current_user', None)
    action = 'CREATE' if created else 'UPDATE'
    create_log(user=user, action=action, inventory=instance)

@receiver(post_delete, sender=Inventory)
def log_inventory_delete(sender, instance, **kwargs):
    user = getattr(instance, '_current_user', None)
    create_log(user=user, action='DELETE', inventory=instance)