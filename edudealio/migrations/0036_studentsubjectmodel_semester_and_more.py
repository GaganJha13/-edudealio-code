# Generated by Django 4.2.6 on 2023-12-20 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edudealio', '0035_aitopicmodel_alter_questionnairemodel_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubjectmodel',
            name='semester',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='studentsubjectmodel',
            name='student_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='edudealio.classmodel'),
        ),
    ]
