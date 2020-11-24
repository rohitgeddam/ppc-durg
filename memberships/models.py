from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here


class Trainer(models.Model):
    trainer_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    dob = models.DateField()
    home_address = models.CharField(max_length=512, null=False, blank=False)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("first_name", "last_name", "mobile_number_1")


class Member(models.Model):
    membership_id = models.CharField(max_length=255, blank=True, null=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    dob = models.DateField()
    wo_ho_so_do = models.CharField(max_length=255, null=False, blank=False)
    home_address = models.CharField(max_length=512, null=False, blank=False)
    mobile_number_1 = models.CharField(max_length=10)
    mobile_number_2 = models.CharField(max_length=10, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, blank=True, null=True, related_name="member"
    )

    is_registeration_done = models.BooleanField(default=False, null=True, blank=True)
    registeration_step = models.IntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("first_name", "last_name", "mobile_number_1")


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
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="disease")
    medical_profile = models.ForeignKey(
        MedicalProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    disease = models.CharField(max_length=255, choices=DISEASE_CHOICE)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(datetime.date.today().year - 100),
            MaxValueValidator(datetime.date.today().year),
        ],
    )

    def __str__(self):
        return f"{self.disease} - {self.member.first_name} {self.member.last_name}"

    class Meta:
        unique_together = ("member", "disease")


@receiver(post_save, sender=Disease)
def post_disease_handler(sender, instance, created, **kwargs):
    if created:
        try:
            instance.medical_profile = instance.member.medical_profile
            instance.save()
        # print("medical_profile", instance.medical_profile)
        except:
            medi_profile = MedicalProfile(member=instance.member)
            medi_profile.save()
            instance.medical_profile = medi_profile
            instance.save()


class Goal(models.Model):
    GOAL_CHOICES = (
        ("to lose weight", "to lose weight"),
        ("to reduce stress", "to reduce stress"),
        ("to improve cardiovascular", "to improve cardiovascular"),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goal")
    goal = models.CharField(max_length=255, choices=GOAL_CHOICES, null=False)
    other_goals = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.first_name + ' ' + self.member.last_name} - {self.goal}"

    class Meta:
        unique_together = ("member", "goal")


class GeneralExamination(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="general_examination"
    )
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
    date_of_examination = models.DateField()


class SystemicExamination(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="systemic_examination"
    )
    cns = models.TextField(null=True, blank=True)
    cvs = models.TextField(null=True, blank=True)
    git = models.TextField(null=True, blank=True)
    rs = models.TextField(null=True, blank=True)
    ent = models.TextField(null=True, blank=True)
    others = models.TextField(null=True, blank=True)

    date_of_examination = models.DateField()


class Fee(models.Model):
    MEMBERSHIP_CHOICES = (
        ("yearly", "yearly"),
        ("half yearly", "half yearly"),
        ("monthly", "monthly"),
    )

    PAYMENT_METHOD = (("cash", "cash"), ("online", "online"))

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="fee")
    payment_type = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    date_of_payment = models.DateField(auto_now_add=True)
    next_due_date = models.DateField(null=True, blank=True)
    amount_paid = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} paid {self.amount_paid} on {self.date_of_payment}"

    @property
    def is_past_due(self):
        if datetime.date.today() > self.next_due_date:
            return True
        return False


@receiver(post_save, sender=Fee)
def post_fee_save(sender, instance, created, **kwargs):
    if created:
        # member = instance.member

        # try:
        #     last_pay_slip = member.fee.order_by("-date_of_payment")[1]

        #     last_due_date = last_pay_slip.next_due_date

        #     days_unused = last_due_date - instance.date_of_payment
        #     if days_unused.days < 0:
        #         days_unused = 0
        #     else:
        #         days_unused = days_unused.days

        # except:
        #     print("ERROR")
        #     days_unused = 0
        # # days_unused = 0
        # print(days_unused, "DLKFJLKFDS")
        try:
            if instance.payment_type == "yearly":
                instance.next_due_date = (
                    instance.date_of_payment
                    + datetime.timedelta(days=365)
                    # + datetime.timedelta(days=days_unused)
                )
            elif instance.payment_type == "half yearly":
                instance.next_due_date = (
                    instance.date_of_payment
                    + datetime.timedelta(days=183)
                    # + datetime.timedelta(days=days_unused)
                )
            else:
                instance.next_due_date = (
                    instance.date_of_payment
                    + datetime.timedelta(days=31)
                    # + datetime.timedelta(days=days_unused)
                )

        except:
            instance.amount_paid = "-1"

        instance.save()
