# Generated by Django 5.0.6 on 2024-06-07 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_bookpatient_delete_patientvital'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='speciality',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]