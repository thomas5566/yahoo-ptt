# Generated by Django 3.2 on 2020-10-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieptt', '0005_auto_20201019_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countgoodandbad',
            name='bad_ray',
            field=models.CharField(blank=True, max_length=255, verbose_name='Bad_ray'),
        ),
        migrations.AlterField(
            model_name='countgoodandbad',
            name='good_ray',
            field=models.CharField(blank=True, max_length=255, verbose_name='Good_ray'),
        ),
    ]
