# Generated by Django 3.2 on 2020-10-16 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movieptt', '0002_alter_movie_approval_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieimage',
            name='movie',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='movieptt.movie'),
        ),
        migrations.AlterField(
            model_name='pttmovie',
            name='key_word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='movieptt.movie'),
        ),
    ]
