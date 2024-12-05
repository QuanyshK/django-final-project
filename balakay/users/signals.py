import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Client, Child, UserSubscription

logger = logging.getLogger('users')

@receiver(post_save, sender=Client)
def log_client_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Client created: {instance.id} - {instance.first_name} {instance.last_name}")
    else:
        logger.info(f"Client updated: {instance.id} - {instance.first_name} {instance.last_name}")

@receiver(post_delete, sender=Client)
def log_client_delete(sender, instance, **kwargs):
    logger.info(f"Client deleted: {instance.id} - {instance.first_name} {instance.last_name}")

@receiver(post_save, sender=Child)
def log_child_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Child created: {instance.id} - {instance.first_name} {instance.last_name}")
    else:
        logger.info(f"Child updated: {instance.id} - {instance.first_name} {instance.last_name}")

@receiver(post_delete, sender=Child)
def log_child_delete(sender, instance, **kwargs):
    logger.info(f"Child deleted: {instance.id} - {instance.first_name} {instance.last_name}")

@receiver(post_save, sender=UserSubscription)
def log_subscription_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Subscription created: {instance.id} - Child: {instance.child.first_name}, Type: {instance.subscription_type}")
    else:
        logger.info(f"Subscription updated: {instance.id} - Child: {instance.child.first_name}, Type: {instance.subscription_type}")

@receiver(post_delete, sender=UserSubscription)
def log_subscription_delete(sender, instance, **kwargs):
    logger.info(f"Subscription deleted: {instance.id} - Child: {instance.child.first_name}, Type: {instance.subscription_type}")
