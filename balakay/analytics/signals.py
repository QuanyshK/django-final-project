import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from centers.models import Center, Booking
# Set up a logger to record information about user, center, and booking changes
logger = logging.getLogger('analytics')

@receiver(post_save, sender=User)
def log_user_registration(sender, instance, created, **kwargs):
    """
        Logs information when a User instance is created.
        This function is triggered when a new user registers.
        """
    if created:
        # If the user is newly created, log the user's ID and username
        logger.info(f"User registered: {instance.id} - {instance.username}")

# Signal receiver for when a User is deleted
@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    """
       Logs information when a User instance is deleted.
       This function is triggered when a user account is deleted.
       """
    # Log the user's ID and username upon deletion
    logger.info(f"User deleted: {instance.id} - {instance.username}")

# Signal receiver for when a Center is saved (i.e., created or updated)
@receiver(post_save, sender=Center)
def log_center_save(sender, instance, created, **kwargs):
    """
        Logs information when a Center instance is saved.
        This function is triggered when a new center is created or an existing center is updated.
        """

    if created:
        # If the center is newly created, log the center's ID, name, and city
        logger.info(f"Center created: {instance.id} - {instance.name}, City: {instance.city}")
    else:
        # If the center is updated, log the center's ID, name, and city
        logger.info(f"Center updated: {instance.id} - {instance.name}, City: {instance.city}")

# Signal receiver for when a Center is deleted
@receiver(post_delete, sender=Center)
def log_center_delete(sender, instance, **kwargs):
    """
        Logs information when a Center instance is deleted.
        This function is triggered when a center is deleted.
        """
    # Log the center's ID, name, and city upon deletion
    logger.info(f"Center deleted: {instance.id} - {instance.name}, City: {instance.city}")

# Signal receiver for when a Booking is saved (i.e., created or updated)
@receiver(post_save, sender=Booking)
def log_booking_save(sender, instance, created, **kwargs):
    """
       Logs information when a Booking instance is saved.
       This function is triggered when a new booking is created or an existing booking is updated.
       """
    if created:
        # If the booking is newly created, log the booking's ID, status, and user associated with the booking
        logger.info(f"Booking created: {instance.id} - Status: {instance.status}, User: {instance.user}")
    else:
        # If the booking is updated, log the booking's ID, status, and user associated with the booking
        logger.info(f"Booking updated: {instance.id} - Status: {instance.status}, User: {instance.user}")

# Signal receiver for when a Booking is deleted
@receiver(post_delete, sender=Booking)
def log_booking_delete(sender, instance, **kwargs):
    """
        Logs information when a Booking instance is deleted.
        This function is triggered when a booking is deleted.
        """
    # Log the booking's ID, status, and user upon deletion
    logger.info(f"Booking deleted: {instance.id} - Status: {instance.status}, User: {instance.user}")
