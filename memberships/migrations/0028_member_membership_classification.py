# Generated by Django 3.1.3 on 2020-11-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0027_auto_20201128_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='membership_classification',
            field=models.CharField(choices=[('Civilian', 'Civilian'), ('Civilian Couples', 'Civilian Couples'), ('Civilian Family Package (H, W, 2C)', 'Civilian Family Package (H, W, 2C)'), ('Civilian Family Package (H, W, 1C)', 'Civilian Family Package (H, W, 1C)'), ('C.G Police, CPO s, BSP, Sail, Other Govt. Emp', 'C.G Police, CPO s, BSP, Sail, Other Govt. Emp'), ('Couples (Gov)', 'Couples (Gov)'), ('Family Package (H, W, 2C) (Gov)', 'Family Package (H, W, 2C) (Gov)'), ('Family Package (H, W, 1C) (Gov)', 'Family Package (H, W, 1C) (Gov)'), ('so/do/wife-of (Gov Emp)', 'so/do/wife-of (Gov Emp)')], default='Civilian', max_length=255),
            preserve_default=False,
        ),
    ]
