# Generated by Django 5.0.6 on 2024-06-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_bookpatient_triage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='time',
            field=models.TimeField(blank=True, null=True, unique=True),
        ),
    ]