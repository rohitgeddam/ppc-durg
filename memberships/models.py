from django.db import models

# Create your models here


class Trainer(models.Model):
    trainer_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    home_address = models.CharField(max_length=512)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        trainer = Trainer.objects.filter(pk=self.pk).first()
        if not trainer:
            last_trainer = Trainer.objects.all().last()
            self.trainer_id = "T" + "{0}".format(str(last_trainer.pk).zfill(4))
        super(Member, self).save(*args, **kwargs)


class Member(models.Model):
    membership_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    wo_ho_so_do = models.CharField(max_length=255)
    home_address = models.CharField(max_length=512)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10)

    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        member = Member.objects.filter(pk=self.pk).first()
        if not member:
            last_member = Member.objects.all().last()
            self.membership_id = "M" + "{0}".format(str(last_member.pk).zfill(6))
        super(Member, self).save(*args, **kwargs)


class Goal(models.Model):
    GOAL_CHOICES = (
        ("to lose weight", "to lose weight"),
        ("to reduce stress", "to reduce stress"),
        ("to improve cardiovascular", "to improve cardiovascular"),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255, choices=GOAL_CHOICES)
    other_goals = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member.first_name + ' ' + self.member.last_name} - {self.goal}"