# Generated by Django 5.0.6 on 2024-05-24 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(upload_to='profile_pictures/')),
                ('religion', models.CharField(blank=True, choices=[('CHRISTIANITY', 'Christianity'), ('ISLAM', 'Islam')], default='CHRISTIANITY', max_length=255, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=255, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('SINGLE', 'Single'), ('MARRIED', 'Married')], default='SINGLE', max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.CharField(blank=True, choices=[('ASHANTI', 'Ashanti'), ('BONO', 'Bono'), ('BONO_EAST', 'Bono East'), ('AHAFO', 'Ahafo'), ('CENTRAL', 'Central'), ('EASTERN', 'Eastern'), ('GREATER_ACCRA', 'Greater Accra'), ('NORTHERN', 'Northern'), ('SAVANNAH', 'Savannah'), ('NORTH_EAST', 'North East'), ('UPPER_EAST', 'Upper East'), ('UPPER_WEST', 'Upper West'), ('VOLTA', 'Volta'), ('OTI', 'Oti'), ('WESTERN', 'Western'), ('WESTERN_NORTH', 'Western North')], default='EASTERN', max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('kin_name', models.CharField(blank=True, max_length=255, null=True)),
                ('kin_address', models.CharField(blank=True, max_length=255, null=True)),
                ('relationship', models.CharField(blank=True, max_length=255, null=True)),
                ('kin_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('kin_email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
