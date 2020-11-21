from django.forms import ModelForm
from memberships import models
from django import forms
from django.forms import modelformset_factory
from django.forms import formset_factory


class MemberForm(ModelForm):
    class Meta:
        model = models.Member
        exclude = [
            "membership_id",
        ]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }


# GoalFormSet = modelformset_factory(
#     models.Goal,
#     exclude=["member", "other_goals"],
#     extra=3,
# )


class GoalForm(ModelForm):
    class Meta:
        model = models.Goal
        exclude = ["member", "other_goals"]


GoalFormSet = formset_factory(GoalForm, extra=2)


class MedicalProfileForm(ModelForm):
    class Meta:
        model = models.MedicalProfile
        exclude = [
            "member",
        ]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }


DiseaseFormset = modelformset_factory(
    models.Disease,
    exclude=["member", "medical_profile"],
    extra=3,
)


class FeeForm(ModelForm):
    class Meta:
        model = models.Fee
        exclude = ["member", "next_due_date", "date_of_payment"]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }
