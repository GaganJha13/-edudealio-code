# Generated by Django 4.2.6 on 2023-11-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edudealio', '0021_rename_expiry_date_offersmodel_validity_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offersmodel',
            name='validity_period',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='studentpointsmodel',
            name='date',
            field=models.DateField(),
        ),
    ]
