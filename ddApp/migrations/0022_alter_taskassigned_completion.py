# Generated by Django 4.2.5 on 2023-09-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0021_alter_taskassigned_beneficiary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskassigned',
            name='completion',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Installation Done!', 'Installation Done!')], default='Initiated', max_length=64),
        ),
    ]