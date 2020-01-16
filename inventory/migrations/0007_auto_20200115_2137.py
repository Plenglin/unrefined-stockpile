# Generated by Django 2.2.2 on 2020-01-16 05:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20200111_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='qr_uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid1),
        ),
        migrations.AddField(
            model_name='item',
            name='qr_uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid1),
        ),
    ]