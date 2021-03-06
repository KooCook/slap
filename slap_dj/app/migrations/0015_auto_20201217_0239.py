# Generated by Django 3.1.3 on 2020-12-17 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20201214_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='wikidata_id',
            field=models.CharField(default='', max_length=13),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.song'),
        ),
    ]
