# Generated by Django 2.1.5 on 2019-10-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0003_auto_20191010_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='pic',
            field=models.CharField(max_length=255, verbose_name='路径图片'),
        ),
    ]
