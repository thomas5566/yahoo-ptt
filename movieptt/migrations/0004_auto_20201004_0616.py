# Generated by Django 3.1 on 2020-10-04 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieptt', '0003_pttmovie_key_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pttmovie',
            name='title',
            field=models.CharField(default=1, max_length=255, unique=True, verbose_name='Title'),
            preserve_default=False,
        ),
    ]
