# Generated by Django 4.2.5 on 2023-09-27 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0031_alter_taskassigned_beneficiary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskassigned',
            name='completion',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Intrans-it', 'Intrans-it'), ('Initiated', 'Initiated'), ('Installation Done!', 'Installation Done!')], default='Initiated', max_length=64),
        ),
    ]
