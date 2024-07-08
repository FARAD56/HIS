from typing import Any
from django.db import models
from users.models import CustomUser
# Create your models here.

class Diagnosis(models.Model):
    class Type(models.TextChoices):
        Chronic = "Chronic"
        Acute = "Acute"

    class Diagnosis(models.TextChoices):
        Headache = "Headache"
        Seizures = "Seizures"
        Diabetes = "Diabetes"
        Hypertension = "Hypertension"
        Depression = "Depression"
        Pneumonia = "Pneumonia"
        Arthritis = "Arthritis"
        Dermathitis = "Dermathitis"
        Back_pain = "Back Pain"

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='patient_diagnosis')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='doctor_diagnosis')
    diagnosis = models.CharField(
            max_length=20, 
            blank=True, 
            null=True,
            choices=Diagnosis.choices,
            default=Diagnosis.Headache
        )
    type = models.CharField(
            max_length=20, 
            blank=True, 
            null=True,
            choices=Type.choices,
            default=Type.Acute
        )
    
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.diagnosis}'
    


class Prescription(models.Model):
    class Medicine(models.TextChoices):
        Paracetamol     =  'Paracetamol'
        Lacosamide      =  'Lacosamide'
        Metformin       =  'Metformin'
        ACE_inhibitors  =  'ACE inhibitors'
        SSR_inhibitors  =  'SSR inhibitors'
        Amoxicillin     =  'Amoxicillin'
        Azathioprines   =  'Azathioprines'
        Hydrocortisones =  'Hydrocortisones'
        Ibuprofen       =  'Ibuprofen'
        Doxycycline     =  'Doxycycline'

    class Strength(models.TextChoices):
        mg_50  = '50mg'
        mg_100 = '100mg'
        mg_200  = '200mg'
        mg_500 = '500mg'
    class Dose(models.TextChoices):
        OD  = 'OD'
        BID = 'BID'
        TID = 'TID'
        QID = 'QID'
    class Duration(models.TextChoices):
        week  =  '1 week'
        weeks_2 = '2 weeks'
        weeks_3 = '3 weeks'
        month_1 = '1 month'
        months_2 = '2 months'
        months_3 = '3 months'

    class Frequency(models.TextChoices):
        Once_Daily = 'Once Daily'
        Two_Times_Daily = 'Two Times Daily'
        Three_Times_Daily = 'Three Times Daily'
        Four_Times_Daily = 'Four Times Daily'

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='patient_prescription')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='doctor_prescription')
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=255,
                                choices=Medicine.choices,
                                blank=True, null=True)
    dose = models.CharField(max_length=255, blank=True,
                            choices=Dose.choices,
                            null=True)
    
    duration = models.CharField(max_length=30,blank=True,null=True)

    strength = models.CharField(max_length=30,blank=True,
                                choices=Strength.choices,
                                null=True)
    quantity  = models.PositiveIntegerField(blank=True,null=True)
    frequency = models.CharField(max_length=255,blank=True,null=True,
                                choices=Frequency.choices,default=Frequency.Once_Daily)
    
    instructions = models.TextField(max_length=255,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.medicine}' 
    

class Investigation(models.Model):
    class Referral(models.TextChoices):
        Korle_Bu_Main_hospital  = 'Korle Bu Main hospital'
        Legon_Hospital          = 'Legon Hospital'
        UG_Medical_center       = 'UG Medical center'
        Accra_Medical_center    = 'Accra Medical center'
        Noguchie_Health_center  = 'Noguchie Health center'

    class Investigation(models.TextChoices):
        Blood_tests   = 'Blood tests'
        Urinalysis    = 'Urinalysis'
        Biopsy        = 'Biopsy'
        Amniocentesis = 'Amniocentesis'
        Thyroid_function_tests = 'Thyroid function tests'

    class Unit(models.TextChoices):
        Pathology    = 'Pathology'
        Cardiology   = 'Cardiology'
        Cardithoracy = 'Cardithoracy'
        Gynaecology  = 'Gynaecology'
        Pediatric    = 'Pediatric'
        Opthometry   = 'Opthometry'

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='patient_investigation')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='doctor_investigation')
    referral_facility = models.CharField(max_length=255, blank=True,
                                        choices=Referral.choices,
                                        default=Referral.Korle_Bu_Main_hospital,
                                        null=True)
    investigation = models.CharField(max_length=255, blank=True,
                                    choices=Investigation.choices,
                                    null=True)
    unit = models.CharField(max_length=255, blank=True,
                            choices=Unit.choices,
                            null=True)
    date = models.DateField(auto_now_add=True)
    reason = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.investigation}'