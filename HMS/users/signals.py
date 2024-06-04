from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,ProfileModel,PatientVital

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
    instance.profilemodel.save()



# Signal to create PatientVitals when a new CustomUser is created
@receiver(post_save, sender=CustomUser)
def create_patient_vitals(sender, instance, created, **kwargs):
    if created:
        patient_vital = PatientVital.objects.create()
        patient_vital.user.add(instance)  # Use add() method for many-to-many relationships
        patient_vital.save()