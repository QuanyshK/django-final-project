import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AgeGroup, Subscription

logger = logging.getLogger('subscriptions')

@receiver(post_save, sender=AgeGroup)
def log_age_group_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"AgeGroup created: {instance.id} - {instance.age_range}")
    else:
        logger.info(f"AgeGroup updated: {instance.id} - {instance.age_range}")

@receiver(post_delete, sender=AgeGroup)
def log_age_group_delete(sender, instance, **kwargs):
    logger.info(f"AgeGroup deleted: {instance.id} - {instance.age_range}")

@receiver(post_save, sender=Subscription)
def log_subscription_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Subscription created: {instance.id} - {instance.name}, Active: {instance.active}")
    else:
        logger.info(f"Subscription updated: {instance.id} - {instance.name}, Active: {instance.active}")

@receiver(post_delete, sender=Subscription)
def log_subscription_delete(sender, instance, **kwargs):
    logger.info(f"Subscription deleted: {instance.id} - {instance.name}")
