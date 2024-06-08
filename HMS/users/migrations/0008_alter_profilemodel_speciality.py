# Generated by Django 5.0.6 on 2024-06-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profilemodel_speciality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='speciality',
            field=models.CharField(blank=True, choices=[('Pathology', 'Pathology'), ('Cardiology', 'Cardiology'), ('Cardithoracy', 'Cardithoracy'), ('Gynaecology', 'Gynaecology'), ('Pediatric', 'Pediatric'), ('Opthometry', 'Opthometry'), ('Neurology', 'Neurology'), ('Neurosurgeon', 'Neurosurgeon'), ('Nephrology', 'Nephrology'), ('Ophthalmology', 'Ophthalmology'), ('Physician Speciality', 'Physician Speciality'), ('Family Medicine', 'Family Medicine'), ('Orthopedics', 'Orthopedics')], max_length=255, null=True),
        ),
    ]