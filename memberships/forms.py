from django.forms import ModelForm
from memberships import models
from django import forms
from django.forms import modelformset_factory
from django.forms import formset_factory


class DateInput(forms.DateInput):
    input_type = "date"


class MemberForm(ModelForm):
    mobile_number_1 = forms.CharField(max_length=10, min_length=10)
    # mobile_number_2 = forms.CharField(max_length=10, min_length=0)

    class Meta:
        model = models.Member
        exclude = [
            "membership_id",
            "is_registeration_done",
            "registeration_step",
        ]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }
        widgets = {
            "dob": DateInput(),
        }


class TrainerForm(ModelForm):
    mobile_number_1 = forms.CharField(max_length=10, min_length=10)
    # mobile_number_2 = forms.CharField(max_length=10, min_length=0)

    class Meta:
        model = models.Trainer
        exclude = [
            "trainer_id",
        ]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }
        widgets = {
            "dob": DateInput(),
        }


class GeneralExamForm(ModelForm):
    class Meta:
        model = models.GeneralExamination
        exclude = [
            "member",
        ]
        widgets = {
            "date_of_examination": DateInput(),
        }


class SystemicExamForm(ModelForm):
    class Meta:
        model = models.SystemicExamination
        exclude = [
            "member",
        ]
        widgets = {
            "date_of_examination": DateInput(),
        }


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
    extra=5,
)


class FeeForm(ModelForm):
    class Meta:
        model = models.Fee
        exclude = ["member", "next_due_date", "date_of_payment"]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }
