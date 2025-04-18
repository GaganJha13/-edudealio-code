# Generated by Django 4.2.6 on 2023-12-01 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import edudealio.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edudealio', '0028_standardizetestmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(default=edudealio.utils.generate_referral_code, max_length=8, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
