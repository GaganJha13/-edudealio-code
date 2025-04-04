# Generated by Django 4.2.6 on 2023-10-26 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edudealio', '0002_subscriptionmodel_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('roll_number', models.CharField(max_length=10)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edudealio.schoolmodel')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edudealio.classmodel')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSubjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.DecimalField(decimal_places=2, max_digits=5)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edudealio.studentmodel')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edudealio.subjectmodel')),
            ],
            options={
                'unique_together': {('student', 'subject')},
            },
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='subjects',
            field=models.ManyToManyField(through='edudealio.StudentSubjectModel', to='edudealio.subjectmodel'),
        ),
        migrations.CreateModel(
            name='ExamCertificateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(upload_to='certificates/')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='edudealio.studentmodel')),
            ],
        ),
    ]
