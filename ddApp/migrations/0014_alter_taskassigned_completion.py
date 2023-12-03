# Generated by Django 4.2.5 on 2023-09-19 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0013_taskassigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskassigned',
            name='completion',
            field=models.CharField(choices=[('Initiated', 'Initiated'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Initiated', max_length=16),
        ),
    ]
