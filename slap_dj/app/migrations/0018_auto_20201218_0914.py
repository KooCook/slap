# Generated by Django 3.1.3 on 2020-12-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20201218_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideo',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]