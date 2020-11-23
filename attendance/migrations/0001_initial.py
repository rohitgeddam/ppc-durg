# Generated by Django 3.1.3 on 2020-11-23 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('memberships', '0021_auto_20201123_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField(auto_now_add=True)),
                ('out_time', models.TimeField(blank=True, null=True)),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_attendance', to='attendance.attendancesheet')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_attendance', to='memberships.trainer')),
            ],
            options={
                'unique_together': {('sheet', 'trainer')},
            },
        ),
        migrations.CreateModel(
            name='MemberAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField(auto_now_add=True)),
                ('out_time', models.TimeField(blank=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_attendance', to='memberships.member')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_attendance', to='attendance.attendancesheet')),
            ],
            options={
                'unique_together': {('sheet', 'member')},
            },
        ),
    ]
