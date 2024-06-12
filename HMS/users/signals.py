from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,ProfileModel

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
    instance.profilemodel.save()

