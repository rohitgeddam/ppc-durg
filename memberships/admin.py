from django.contrib import admin
from memberships import models

# Register your models here.

admin.site.register(models.Trainer)
admin.site.register(models.Member)
admin.site.register(models.Goal)
admin.site.register(models.Disease)
admin.site.register(models.MedicalProfile)