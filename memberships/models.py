from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here


class Trainer(models.Model):
    trainer_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=True)
    home_address = models.CharField(max_length=512)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Member(models.Model):
    membership_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dob = models.DateField(null=True)
    wo_ho_so_do = models.CharField(max_length=255)
    home_address = models.CharField(max_length=512)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10)

    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=Member)
def post_member_save(sender, instance, created, **kwargs):
    print("member", created)
    if created:
        try:
            last_member = Member.objects.all().last()
            instance.membership_id = "M" + "{0}".format(str(last_member.pk).zfill(6))
        except:
            instance.membership_id = "-1"

        instance.save()


@receiver(post_save, sender=Trainer)
def post_trainer_save(sender, instance, created, **kwargs):
    if created:
        try:
            last_member = Trainer.objects.all().last()
            instance.trainer_id = "T" + "{0}".format(str(last_member.pk).zfill(4))
        except:
            instance.trainer_id = "-1"

        instance.save()


class MedicalProfile(models.Model):
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE, related_name="medical_profile"
    )

    surgery_history = models.TextField(null=True, blank=True)
    family_disease_history = models.TextField(null=True, blank=True)
    hospitalized_history = models.TextField(null=True, blank=True)

    chronic_ear_disease = models.TextField(null=True, blank=True)
    addiction_history = models.TextField(null=True, blank=True)
    thyroid_history = models.TextField(null=True, blank=True)
    prolonged_drug_intake_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name}'s profile "


class Disease(models.Model):
    DISEASE_CHOICE = (
        ("tuberculosis", "tuberculosis"),
        ("diabetes", "diabetes"),
        ("bronchitis asthama", "bronchitis asthama"),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    medical_profile = models.ForeignKey(
        MedicalProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    disease = models.CharField(max_length=255, choices=DISEASE_CHOICE)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(datetime.date.today().year - 100),
            MaxValueValidator(datetime.date.today().year),
        ]
    )

    def __str__(self):
        return f"{self.disease} - {self.member.first_name} {self.member.last_name}"


@receiver(post_save, sender=Disease)
def post_disease_handler(sender, instance, created, **kwargs):
    if created:
        try:
            instance.medical_profile = instance.member.medical_profile
        # print("medical_profile", instance.medical_profile)
        except:
            MedicalProfile(member=instance.member).save()
            instance.medical_profile = instance.member.medical_profile


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


class GeneralExamination(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    blood_pressure = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(200),
        ],
        null=True,
        blank=True,
    )
    pulse = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        null=True,
        blank=True,
    )

    height = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        null=True,
        blank=True,
    )

    weight = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        null=True,
        blank=True,
    )

    chest_unexpanded = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        null=True,
        blank=True,
    )
    chest_expanded = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300),
        ],
        null=True,
        blank=True,
    )
    others = models.TextField(null=True, blank=True)


class SystemicExamination(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    cns = models.TextField(null=True, blank=True)
    cvs = models.TextField(null=True, blank=True)
    git = models.TextField(null=True, blank=True)
    rs = models.TextField(null=True, blank=True)
    ent = models.TextField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)