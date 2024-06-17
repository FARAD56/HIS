from django.db import models

# Create your models here.

# class Diagnosis(models.Model):
#     class Type(models.TextChoices):
#         CHRONIC = "CHRONIC"
#         ACUTE = "ACUTE"

#     class Diagnosis(models.TextChoices):
#         HEADACHE = "HEADACHE"
#         SEIZURES = "SEIZURES"
#         DIABETES = "DIABETES"
#         HYPERTENSION = "HYPERTENSION"
#         DEPRESSION = "DEPRESSION"
#         PNEUMONIA = "PNEUMONIA"
#         ARTHRITIS = "ARTHRITIS"
#         DERMATHITIS = "DERMATHITIS"
#         BACK_PAIN = "BACK_PAIN"
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     diagnosis = models.CharField(
#             max_length=20, 
#             blank=True, 
#             null=True,
#             choices=Diagnosis.choices,
#             default=Diagnosis.HEADACHE
#         )
#     type = models.CharField(
#             max_length=20, 
#             blank=True, 
#             null=True,
#             choices=Type.choices,
#             default=Type.ACUTE
#         )
    
#     date_created = models.DateTimeField(auto_now_add= True)

#     def __str__(self):
#         return f'Diagnosis for {self.user} at {self.date_created}'
    


# class Prescription(models.Model):
#     class Medicine(models.TextChoices):
#         Paracetamol     =  'Paracetamol    '
#         Lacosamide      =  'Lacosamide     '
#         Metformin       =  'Metformin      '
#         ACE_inhibitors  =  'ACE_inhibitors '
#         SSR_inhibitors  =  'SSR_inhibitors '
#         Amoxicillin     =  'Amoxicillin    '
#         Azathioprines   =  'Azathioprines  '
#         Hydrocortisones =  'Hydrocortisones'
#         Ibuprofen       =  'Ibuprofen      '
#         Doxycycline     =  'Doxycycline    '

#     class Strength(models.TextChoices):
#         mg  = '50mg '
#         m_g = '100mg'
#         Mg  = '200mg'
#         M_g = '500mg'
#     class Dose(models.TextChoices):
#         OD  = 'OD '
#         BID = 'BID'
#         TID = 'TID'
#         QID = 'QID'
#     class Duration(models.TextChoices):
#         week  =  '1 week'
#         weeks_2 = '2 weeks '
#         weeks_3 = '3 weeks '
#         month_1 = '1 month '
#         months_2 = '2 months'
#         months_3 = '3 months'

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
#     medicine = models.CharField(max_length=255,
#                                 choices=Medicine.choices,
#                                 blank=True, null=True)
#     dose = models.CharField(max_length=255, blank=True,
#                             choices=Dose.choices,
#                             null=True)
    
#     duration = models.CharField(max_length=30,blank=True,null=True)

#     strength = models.CharField(max_length=30,blank=True,
#                                 choices=Strength.choices,
#                                 null=True)
#     quatity  = models.PositiveIntegerField(blank=True,null=True)
#     frequency = models.CharField(max_length=255,blank=True,null=True)
#     instructions = models.TextField(max_length=255,blank=True,null=True)
#     date_created = models.DateTimeField(auto_now_add= True)

#     def __str__(self):
#         return f'Prescription for {self.user} at {self.date_created}' 
    

# class Investigation(models.Model):
#     class Referral(models.TextChoices):
#         Korle_Bu_Main_hospital  = 'Korle Bu Main hospital '
#         Legon_Hospital          = 'Legon Hospital'
#         UG_Medical_center       = 'UG Medical center'
#         Accra_Medical_center    = 'Accra Medical center '
#         Noguchie_Health_center  = 'Noguchie Health center'

#     class Investigation(models.TextChoices):
#         Blood_tests   = 'Blood tests  '
#         Urinalysis    = 'Urinalysis   '
#         Biopsy        = 'Biopsy       '
#         Amniocentesis = 'Amniocentesis'
#         Thyroid_function_tests = 'Thyroid function tests'

#     class Unit(models.TextChoices):
#         Pathology    = 'Pathology   '
#         Cardiology   = 'Cardiology  '
#         Cardithoracy = 'Cardithoracy'
#         Gynaecology  = 'Gynaecology '
#         Pediatric    = 'Pediatric   '
#         Opthometry   = 'Opthometry  '

#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     referral_facility = models.CharField(max_length=255, blank=True,
#                                         choices=Referral.choices,
#                                         default=Referral.Korle_Bu_Main_hospital,
#                                         null=True)
#     investigation = models.CharField(max_length=255, blank=True,
#                                     choices=Investigation.choices,
#                                     null=True)
#     unit = models.CharField(max_length=255, blank=True,
#                             choices=Unit.choices,
#                             null=True)
#     date = models.DateField(blank=True, null=True)
#     reason = models.TextField(max_length=255, blank=True, null=True)