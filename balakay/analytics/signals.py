import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from centers.models import Center, Booking

logger = logging.getLogger('analytics')

@receiver(post_save, sender=User)
def log_user_registration(sender, instance, created, **kwargs):
    if created:
        logger.info(f"User registered: {instance.id} - {instance.username}")

@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    logger.info(f"User deleted: {instance.id} - {instance.username}")

@receiver(post_save, sender=Center)
def log_center_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Center created: {instance.id} - {instance.name}, City: {instance.city}")
    else:
        logger.info(f"Center updated: {instance.id} - {instance.name}, City: {instance.city}")

@receiver(post_delete, sender=Center)
def log_center_delete(sender, instance, **kwargs):
    logger.info(f"Center deleted: {instance.id} - {instance.name}, City: {instance.city}")

@receiver(post_save, sender=Booking)
def log_booking_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Booking created: {instance.id} - Status: {instance.status}, User: {instance.user}")
    else:
        logger.info(f"Booking updated: {instance.id} - Status: {instance.status}, User: {instance.user}")

@receiver(post_delete, sender=Booking)
def log_booking_delete(sender, instance, **kwargs):
    logger.info(f"Booking deleted: {instance.id} - Status: {instance.status}, User: {instance.user}")
