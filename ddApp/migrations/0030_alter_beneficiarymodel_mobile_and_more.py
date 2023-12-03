# Generated by Django 4.2.5 on 2023-09-25 16:07

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0029_beneficiarymodel_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='IN'),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='pincode',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Enter a valid 6-digit PIN code.')]),
        ),
    ]
