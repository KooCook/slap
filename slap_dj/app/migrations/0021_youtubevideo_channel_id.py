# Generated by Django 3.1.3 on 2020-12-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_song_genius_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='channel_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
