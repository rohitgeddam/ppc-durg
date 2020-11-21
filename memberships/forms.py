from django.forms import ModelForm
from memberships import models
from django import forms


class MemberForm(ModelForm):
    class Meta:
        model = models.Member
        exclude = [
            "membership_id",
        ]
        # widgets = {
        #     "wo_ho_so_do": forms.CharField(attrs={"cols": 80, "rows": 20}),
        # }
