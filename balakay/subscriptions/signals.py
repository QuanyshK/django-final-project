import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AgeGroup, Subscription

# Configure a logger specifically for the subscriptions app
logger = logging.getLogger('subscriptions')

# Signal receiver for saving (create or update) AgeGroup instances
@receiver(post_save, sender=AgeGroup)
def log_age_group_save(sender, instance, created, **kwargs):
    if created:
        # Log message for AgeGroup creation
        logger.info(f"AgeGroup created: {instance.id} - {instance.age_range}")
    else:
        # Log message for AgeGroup update
        logger.info(f"AgeGroup updated: {instance.id} - {instance.age_range}")

# Signal receiver for deleting AgeGroup instances
@receiver(post_delete, sender=AgeGroup)
def log_age_group_delete(sender, instance, **kwargs):
    logger.info(f"AgeGroup deleted: {instance.id} - {instance.age_range}")

# Signal receiver for saving (create or update) Subscription instances
@receiver(post_save, sender=Subscription)
def log_subscription_save(sender, instance, created, **kwargs):
    if created:
        # Log message for Subscription creation
        logger.info(f"Subscription created: {instance.id} - {instance.name}, Active: {instance.active}")
    else:
        # Log message for Subscription update
        logger.info(f"Subscription updated: {instance.id} - {instance.name}, Active: {instance.active}")

# Signal receiver for deleting Subscription instances
@receiver(post_delete, sender=Subscription)
def log_subscription_delete(sender, instance, **kwargs):
    logger.info(f"Subscription deleted: {instance.id} - {instance.name}")
