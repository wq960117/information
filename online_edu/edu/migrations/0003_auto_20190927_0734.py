# Generated by Django 2.1.4 on 2019-09-27 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0002_auto_20190926_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlevelcondition',
            name='time',
            field=models.IntegerField(verbose_name='时长'),
        ),
    ]
