from django.contrib import admin
from attendance import models

# Register your models here.

admin.site.register(models.AttendanceSheet)
admin.site.register(models.MemberAttendance)
admin.site.register(models.TrainerAttendance)