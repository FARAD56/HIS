# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.core.validators import FileExtensionValidator



from . utils import generate_profile_id

class CustomUser(AbstractUser):
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_id = models.CharField(max_length=20,blank=True,default=generate_profile_id,null=True)
    contact = models.CharField(max_length=20, blank=True,null=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)
    email = models.EmailField(unique=True,max_length=100,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email if self.email else self.username
    
    @property
    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year
        return None
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name}' + ' ' + f'{self.last_name}'
    
# models.py

class ProfileModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.png',upload_to='profile_pictures/',validators=[FileExtensionValidator(['png','jpg'])])
    class MaritalStatus(models.TextChoices):
        SINGLE = "SINGLE"
        MARRIED = "MARRIED"

    class Religion(models.TextChoices):
        CHRISTIANITY = "CHRISTIANITY"
        ISLAM = "ISLAM"
    class Region(models.TextChoices):
        ASHANTI = "ASHANTI"
        BONO  = "BONO"
        BONO_EAST = "BONO_EAST"
        AHAFO = "AHAFO"
        CENTRAL = "CENTRAL"
        EASTERN = "EASTERN"
        GREATER_ACCRA = "GREATER_ACCRA"
        NORTHERN = "NORTHERN" 
        SAVANNAH = "SAVANNAH"
        NORTH_EAST = "NORTH_EAST"
        UPPER_EAST  = "UPPER_EAST"
        UPPER_WEST = "UPPER_WEST"
        VOLTA = "VOLTA" 
        OTI = "OTI" 
        WESTERN = "WESTERN" 
        WESTERN_NORTH = "WESTERN_NORTH"

    religion = models.CharField(max_length=255, 
                                blank=True, 
                                null=True,
                                choices=Religion.choices,
                                default=Religion.CHRISTIANITY)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=255,
                                      blank=True,
                                      null=True,
                                      choices=MaritalStatus.choices,
                                      default=MaritalStatus.SINGLE)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, 
                              blank=True, 
                              null=True,
                              choices=Region.choices,
                              default=Region.EASTERN)
    address = models.CharField(max_length=255, blank=True, null=True)

    #KIN DETAILS
    kin_name = models.CharField(max_length=255, blank=True, null=True)
    kin_address = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    kin_contact = models.CharField(max_length=255, blank=True, null=True)
    kin_email = models.EmailField(unique=True, blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
