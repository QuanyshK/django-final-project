import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category, Center, Section, Schedule, Booking, FavoriteSection

logger = logging.getLogger('centers')

@receiver(post_save, sender=Category)
def log_category_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Category created: {instance.id} - {instance.name}")
    else:
        logger.info(f"Category updated: {instance.id} - {instance.name}")

@receiver(post_delete, sender=Category)
def log_category_delete(sender, instance, **kwargs):
    logger.info(f"Category deleted: {instance.id} - {instance.name}")

@receiver(post_save, sender=Center)
def log_center_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Center created: {instance.id} - {instance.name}")
    else:
        logger.info(f"Center updated: {instance.id} - {instance.name}")

@receiver(post_delete, sender=Center)
def log_center_delete(sender, instance, **kwargs):
    logger.info(f"Center deleted: {instance.id} - {instance.name}")

@receiver(post_save, sender=Section)
def log_section_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Section created: {instance.id} - {instance.name}")
    else:
        logger.info(f"Section updated: {instance.id} - {instance.name}")

@receiver(post_delete, sender=Section)
def log_section_delete(sender, instance, **kwargs):
    logger.info(f"Section deleted: {instance.id} - {instance.name}")

@receiver(post_save, sender=Schedule)
def log_schedule_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Schedule created: {instance.id} - Section: {instance.section.name}, Start: {instance.start_time}")
    else:
        logger.info(f"Schedule updated: {instance.id} - Section: {instance.section.name}, Start: {instance.start_time}")

@receiver(post_delete, sender=Schedule)
def log_schedule_delete(sender, instance, **kwargs):
    logger.info(f"Schedule deleted: {instance.id} - Section: {instance.section.name}")

@receiver(post_save, sender=Booking)
def log_booking_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Booking created: {instance.id} - User: {instance.user}, Section: {instance.schedule.section.name}")
    else:
        logger.info(f"Booking updated: {instance.id} - User: {instance.user}, Section: {instance.schedule.section.name}")

@receiver(post_delete, sender=Booking)
def log_booking_delete(sender, instance, **kwargs):
    logger.info(f"Booking deleted: {instance.id} - User: {instance.user}, Section: {instance.schedule.section.name}")

@receiver(post_save, sender=FavoriteSection)
def log_favorite_section_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"FavoriteSection created: {instance.id} - Client: {instance.client.user.username}, Section: {instance.section.name}")
    else:
        logger.info(f"FavoriteSection updated: {instance.id} - Client: {instance.client.user.username}, Section: {instance.section.name}")

@receiver(post_delete, sender=FavoriteSection)
def log_favorite_section_delete(sender, instance, **kwargs):
    logger.info(f"FavoriteSection deleted: {instance.id} - Client: {instance.client.user.username}, Section: {instance.section.name}")
