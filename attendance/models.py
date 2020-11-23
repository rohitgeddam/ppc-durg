from django.db import models

from memberships.models import Member, Trainer

# Create your models here.
class AttendanceSheet(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)

    def __str__(self):
        return f"{self.date}"


class MemberAttendance(models.Model):
    sheet = models.ForeignKey(
        AttendanceSheet, on_delete=models.CASCADE, related_name="member_attendance"
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="member_attendance"
    )
    in_time = models.TimeField(auto_now_add=True)
    out_time = models.TimeField(blank=True, null=True)

    class Meta:
        unique_together = ("sheet", "member")

    def __str__(self):
        return f"{self.sheet.date} - {self.member.membership_id}"


class TrainerAttendance(models.Model):
    sheet = models.ForeignKey(
        AttendanceSheet, on_delete=models.CASCADE, related_name="trainer_attendance"
    )
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="trainer_attendance"
    )
    in_time = models.TimeField(auto_now_add=True)
    out_time = models.TimeField(blank=True, null=True)

    class Meta:
        unique_together = ("sheet", "trainer")

    def __str__(self):
        return f"{self.sheet.date} - {self.trainer.trainer_id}"
