import os
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Doctor, Hospital
from ..accounts.models import User


@receiver(post_save, sender=Doctor)
@receiver(post_save, sender=Hospital)
@receiver(post_save, sender=User)
def image_create(instance, created, **kwargs):
    if created:
        old_path = instance.photo.path
        if old_path != (settings.MEDIA_ROOT + 'photos/default.png').replace('/', '\\'):
            directory = old_path[:old_path.rfind('\\')]
            new_path = directory + '\\' + str(instance.id) + '.png'
            os.rename(old_path, new_path)
            instance.photo = new_path
            instance.save()


@receiver(post_delete, sender=Doctor)
@receiver(post_delete, sender=Hospital)
@receiver(post_delete, sender=User)
def image_delete(instance, **kwargs):
    path = instance.photo.path
    if path != (settings.MEDIA_ROOT + 'photos/default.png').replace('/', '\\'):
        os.remove(path)
