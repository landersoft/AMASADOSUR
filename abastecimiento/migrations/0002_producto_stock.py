# Generated by Django 2.2 on 2019-04-25 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastecimiento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
