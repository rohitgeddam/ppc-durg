# Generated by Django 3.1.3 on 2020-11-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0010_auto_20201121_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='goal',
            field=models.CharField(choices=[('to lose weight', 'to lose weight'), ('to reduce stress', 'to reduce stress'), ('to improve cardiovascular', 'to improve cardiovascular')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='dob',
            field=models.DateField(default='2000-05-08'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='dob',
            field=models.DateField(default='2000-05-08'),
        ),
    ]
