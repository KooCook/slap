# Generated by Django 3.1.3 on 2020-12-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201206_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcache',
            name='word',
            field=models.CharField(max_length=289, unique=True),
        ),
    ]
