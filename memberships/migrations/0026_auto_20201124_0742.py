# Generated by Django 3.1.3 on 2020-11-24 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0025_auto_20201124_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(default='default.png', upload_to='profile_pic'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='profile_pic',
            field=models.ImageField(default='default.png', upload_to='profile_pic'),
        ),
    ]