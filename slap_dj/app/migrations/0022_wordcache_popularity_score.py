# Generated by Django 3.1.3 on 2020-12-19 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_youtubevideo_channel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordcache',
            name='popularity_score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
