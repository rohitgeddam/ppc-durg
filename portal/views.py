from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView
from memberships.models import (
    Member,
    MedicalProfile,
    Disease,
    Goal,
    GeneralExamination,
    SystemicExamination,
)
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat


from memberships.forms import (
    MemberForm,
    GoalForm,
    MedicalProfileForm,
    DiseaseFormset,
    FeeForm,
)

# Create your views here.
class MemberList(ListView):
    model = Member
    template_name = "portal/members/list.html"
    context_object_name = "members_list"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = self.model.objects.annotate(
                full_name=Concat("first_name", V(" "), "last_name")
            ).filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(membership_id__icontains=query)
                | Q(full_name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


def memberProfileView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    goals = member.goal.all()
    diseases = member.disease.all()
    medical_profile = member.medical_profile
    systemic_examination = member.systemic_examination.all()
    general_examination = member.general_examination.all()

    context = {
        "goals": goals,
        "member": member,
        "diseases": diseases,
        "medical_profile": medical_profile,
        "systemic_examination": systemic_examination,
        "general_examination": general_examination,
        "member_pk": pk,
    }

    return render(request, "portal/members/detail.html", context)


# class MemberDetailsUpdate(UpdateView):
#     model = Member
#     form_class = MemberForm
#     template_name = "member_details_update.html"
#     success_url = reverse("members_profile")
