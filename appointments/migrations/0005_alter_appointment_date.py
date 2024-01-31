# Generated by Django 4.2.9 on 2024-01-31 08:43

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_alter_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='eg. 23-11-2023', validators=[django.core.validators.MinValueValidator(datetime.datetime(2024, 1, 31, 8, 43, 11, 322432, tzinfo=datetime.timezone.utc)), django.core.validators.MaxValueValidator(datetime.datetime(2024, 3, 1, 8, 43, 11, 322432, tzinfo=datetime.timezone.utc))]),
        ),
    ]