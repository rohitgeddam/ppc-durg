# Generated by Django 3.1.3 on 2020-11-21 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0006_auto_20201121_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]