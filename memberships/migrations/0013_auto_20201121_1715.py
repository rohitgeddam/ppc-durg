# Generated by Django 3.1.3 on 2020-11-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0012_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='next_due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]