from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,ProfileModel,BookPatient

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
    instance.profilemodel.save()



# Signal to create BookPatient when a new CustomUser is created
# @receiver(post_save, sender=CustomUser)
# def create_book_patient(sender, instance, created, **kwargs):
#     if created:
#         BookPatient.objects.create(user=instance)