# Generated by Django 3.2.4 on 2022-05-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_athlete_favorite_sports'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepicture',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='آیا فعال است؟'),
        ),
    ]