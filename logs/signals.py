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

# Purchases signals
@receiver(post_save, sender=Purchases)
def log_purchase_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_current_user', None)
    action = 'CREATE' if created else 'UPDATE'
    create_log(user=user, action=action, purchase=instance)

@receiver(post_delete, sender=Purchases)
def log_purchase_delete(sender, instance, **kwargs):
    user = getattr(instance, '_current_user', None)
    create_log(user=user, action='DELETE', purchase=instance)


# Servicing signals
@receiver(post_save, sender=Servicing)
def log_servicing_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_current_user', None)
    action = 'CREATE' if created else 'UPDATE'
    create_log(user=user, action=action, servicing=instance)

@receiver(post_delete, sender=Servicing)
def log_servicing_delete(sender, instance, **kwargs):
    user = getattr(instance, '_current_user', None)
    create_log(user=user, action='DELETE', servicing=instance)


# Rentals signals
@receiver(post_save, sender=Rentals)
def log_rental_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_current_user', None)
    action = 'CREATE' if created else 'UPDATE'
    create_log(user=user, action=action, rental=instance)

@receiver(post_delete, sender=Rentals)
def log_rental_delete(sender, instance, **kwargs):
    user = getattr(instance, '_current_user', None)
    create_log(user=user, action='DELETE', rental=instance)


# Disposals signals
@receiver(post_save, sender=Disposals)
def log_disposal_save(sender, instance, created, **kwargs):
    user = getattr(instance, '_current_user', None)
    action = 'CREATE' if created else 'UPDATE'
    create_log(user=user, action=action, disposal=instance)

@receiver(post_delete, sender=Disposals)
def log_disposal_delete(sender, instance, **kwargs):
    user = getattr(instance, '_current_user', None)
    create_log(user=user, action='DELETE', disposal=instance)