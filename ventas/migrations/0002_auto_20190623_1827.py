# Generated by Django 2.2.2 on 2019-06-23 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleventa',
            old_name='precio_venta',
            new_name='precio_venta_unitario',
        ),
    ]