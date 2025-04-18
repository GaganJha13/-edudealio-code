# Generated by Django 4.2.6 on 2023-10-27 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edudealio', '0004_rename_marks_studentsubjectmodel_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolmodel',
            name='location',
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='exam_certificate',
            field=models.FileField(null=True, upload_to='exam_certificates/'),
        ),
        migrations.AddField(
            model_name='subjectmodel',
            name='associated_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='edudealio.classmodel'),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='subjects',
            field=models.ManyToManyField(related_name='students', through='edudealio.StudentSubjectModel', to='edudealio.subjectmodel'),
        ),
        migrations.DeleteModel(
            name='ExamCertificateModel',
        ),
    ]
