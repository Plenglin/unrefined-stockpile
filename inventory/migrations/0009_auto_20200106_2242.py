# Generated by Django 2.2.2 on 2020-01-07 06:42

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20200105_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='location_metadata',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='item',
            name='location_metadata',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
    ]