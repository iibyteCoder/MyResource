# Generated by Django 2.2.9 on 2020-02-07 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myresource', '0004_auto_20200206_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyroutine',
            name='event_special',
            field=models.CharField(default='no', max_length=16),
        ),
    ]
