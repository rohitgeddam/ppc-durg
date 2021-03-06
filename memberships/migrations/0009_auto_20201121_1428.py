# Generated by Django 3.1.3 on 2020-11-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0008_auto_20201121_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemicexamination',
            name='member',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='addiction_history',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='chronic_ear_disease',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='family_disease_history',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='hospitalized_history',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='prolonged_drug_intake_history',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='surgery_history',
        ),
        migrations.RemoveField(
            model_name='medicalprofile',
            name='thyroid_history',
        ),
        migrations.AlterField(
            model_name='member',
            name='dob',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='GeneralExamination',
        ),
        migrations.DeleteModel(
            name='SystemicExamination',
        ),
    ]
