# Generated by Django 3.1.3 on 2020-11-24 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0024_auto_20201124_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_registeration_done',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='registeration_step',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
