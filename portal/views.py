from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from memberships.models import (
    Member,
    MedicalProfile,
    Disease,
    Goal,
    GeneralExamination,
    SystemicExamination,
    Trainer,
    Fee,
)
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from django.http import HttpResponseRedirect
from memberships.forms import (
    MemberForm,
    GoalForm,
    GoalFormSet,
    MedicalProfileForm,
    DiseaseFormset,
    FeeForm,
    GeneralExamForm,
    SystemicExamForm,
)

import datetime

from attendance.models import AttendanceSheet, MemberAttendance, TrainerAttendance

# Create your views here.
class MemberList(LoginRequiredMixin, ListView):
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
                | Q(mobile_number_1__icontains=query)
                | Q(mobile_number_2__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


class TrainerList(LoginRequiredMixin, ListView):
    model = Trainer
    template_name = "portal/members/trainer_list.html"
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
                | Q(trainer_id__icontains=query)
                | Q(full_name__icontains=query)
                | Q(mobile_number_1__icontains=query)
                | Q(mobile_number_2__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list


@login_required
def memberProfileView(request, pk):
    member = Member.objects.filter(pk=pk).first()

    if not member.is_registeration_done:
        return HttpResponseRedirect(
            reverse(f"registerstep{member.registeration_step}", args=[pk])
        )

    goals = member.goal.all()
    diseases = member.disease.all()
    medical_profile = member.medical_profile
    systemic_examination = member.systemic_examination.all().order_by(
        "-date_of_examination"
    )
    general_examination = member.general_examination.all().order_by(
        "-date_of_examination"
    )
    fees = member.fee.all().order_by("-next_due_date")
    context = {
        "goals": goals,
        "member": member,
        "diseases": diseases,
        "medical_profile": medical_profile,
        "systemic_examination": systemic_examination,
        "general_examination": general_examination,
        "fees": fees,
        "member_pk": pk,
    }

    return render(request, "portal/members/detail.html", context)


class MemberDetailsUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "portal/members/member_details_update.html"
    context_object_name = "object"

    def get_success_url(self):

        memberPk = self.kwargs["pk"]
        return reverse_lazy("members_profile", kwargs={"pk": memberPk})


@login_required
def goalCreateView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = GoalFormSet(
            request.POST,
        )
        if formset.is_valid():

            # do something with the formset.cleaned_data
            for form in formset:
                if form.cleaned_data != {}:
                    try:
                        form.save(commit=False)
                        form.instance.member = member
                        form.save()
                    except:
                        continue

            return HttpResponseRedirect(reverse_lazy("members_profile", args=[pk]))
            # return render(request, "memberships/registeration_done.html")

    else:
        formset = GoalFormSet()
    return render(
        request,
        "portal/members/member_add_goal.html",
        {"form": formset, "member_id": pk},
    )


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    # fields = "__all__"
    form_class = GoalForm
    template_name = "portal/members/member_goal_update.html"
    context_object_name = "object"

    def get_success_url(self):

        memberPk = self.kwargs["memberId"]
        return reverse_lazy("members_profile", kwargs={"pk": memberPk})


class MedicalProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalProfile
    # fields = "__all__"
    form_class = MedicalProfileForm
    template_name = "portal/members/member_medical_profile_update.html"
    context_object_name = "object"

    def get_success_url(self):

        memberPk = self.kwargs["memberId"]
        return reverse_lazy("members_profile", kwargs={"pk": memberPk})


@login_required
def diseaseAddView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = DiseaseFormset(
            request.POST,
            queryset=Disease.objects.none(),
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            for form in formset:
                # form.save(commit=False)
                if form.cleaned_data != {}:
                    try:
                        form.instance.member = member
                        form.save()
                    except:
                        continue

            return HttpResponseRedirect(reverse_lazy("members_profile", args=[pk]))
    else:
        formset = DiseaseFormset(
            queryset=Disease.objects.none(),
        )
    return render(
        request,
        "portal/members/member_disease_add.html",
        {"form": formset, "member_id": pk},
    )


@login_required
def GeneralExamCreateView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        form = GeneralExamForm(
            request.POST,
        )
        if form.is_valid():
            # do something with the formset.cleaned_data

            form.instance.member = member
            form.save()

            return HttpResponseRedirect(reverse_lazy("members_profile", args=[pk]))
    else:
        form = GeneralExamForm()
    return render(
        request,
        "portal/members/member_general_exam_add.html",
        {"form": form, "member_id": pk},
    )


@login_required
def SystemicExamCreateView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        form = SystemicExamForm(
            request.POST,
        )
        if form.is_valid():
            # do something with the formset.cleaned_data

            form.instance.member = member
            form.save()

            return HttpResponseRedirect(reverse_lazy("members_profile", args=[pk]))
    else:
        form = SystemicExamForm()
    return render(
        request,
        "portal/members/member_systemic_exam_add.html",
        {"form": form, "member_id": pk},
    )


class PendingFeeList(LoginRequiredMixin, ListView):
    model = Member
    template_name = "portal/fee/pending_list.html"
    context_object_name = "members_list"
    # paginate_by = 20

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
                | Q(mobile_number_1__icontains=query)
                | Q(mobile_number_2__icontains=query)
            )

        else:
            object_list = self.model.objects.all()
        return object_list


class FeeList(LoginRequiredMixin, ListView):
    model = Member
    template_name = "portal/fee/list.html"
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
                | Q(mobile_number_1__icontains=query)
                | Q(mobile_number_2__icontains=query)
            )

        else:
            object_list = self.model.objects.all()
        return object_list


@login_required
def PayFee(request, pk):
    member = Member.objects.filter(pk=pk).first()
    last_fee = Fee.objects.last()

    if request.method == "POST":
        form = FeeForm(
            request.POST,
        )
        if form.is_valid():
            # do something with the formset.cleaned_data
            # payment_type = form.cleaned_data["payment_type"]
            # date_of_payment = datetime.date.today()
            # last_pay_slip = member.fee.order_by("-date_of_payment")[1]
            # last_due_date = last_pay_slip.next_due_date

            # unused_days =
            # if payment_type == "yearly":
            #     form.instance.next_due_date = date_of_payment + datetime.timedelta(
            #         days=365
            #     )
            # elif payment_type == "half yearly":
            #     form.instance.next_due_date = date_of_payment + datetime.timedelta(
            #         days=183
            #     )
            # else:
            #     form.instance.next_due_date = date_of_payment + datetime.timedelta(
            #         days=31
            #     )
            form.instance.initial_date = last_fee.next_due_date
            form.instance.member = member
            form.save()

            return HttpResponseRedirect(reverse_lazy("members_profile", args=[pk]))
    else:
        form = FeeForm()
    return render(
        request,
        "portal/fee/pay.html",
        {"form": form, "member_id": pk, "member": member},
    )


@login_required
def DashboardView(request):
    members = Member.objects.all()
    trainers = Trainer.objects.all()
    sheet = AttendanceSheet.objects.filter(date=datetime.date.today()).first()
    fees = Fee.objects.all()
    attendance_started = False
    try:
        attendance_started = True

        members_attended = sheet.member_attendance.count()
        members_present_attendance = 100 * (members_attended / members.count())
        trainers_attended = sheet.trainer_attendance.count()
        trainers_present_attendance = 100 * (trainers_attended / trainers.count())

    except:
        members_attended = 0
        members_present_attendance = 0
        trainers_attended = 0
        trainers_present_attendance = 0

    total_revenue = 0
    # calculate total revenue
    for fee in fees:
        total_revenue = total_revenue + fee.amount_paid

    context = {
        "members": members,
        "trainers": trainers,
        "attendance_started": attendance_started,
        "sheet": sheet,
        "members_attended": members_attended,
        "members_present_attendance": members_present_attendance,
        "trainers_attended": trainers_attended,
        "trainers_present_attendance": trainers_present_attendance,
        "total_revenue": total_revenue,
    }
    return render(request, "portal/dashboard.html", context)


@login_required
def print_card(request, pk):
    member = Member.objects.filter(pk=pk).first()
    context = {"member": member}
    return render(request, "portal/card.html", context)


@login_required
def print_fee_recipt(request, fee_id):
    fee_slip = Fee.objects.filter(pk=fee_id).first()

    context = {"fee": fee_slip}
    return render(request, "portal/fee_print.html", context)


@login_required
def print_trainer_card(request, pk):
    trainer = Trainer.objects.filter(pk=pk).first()
    context = {"trainer": trainer}
    return render(request, "portal/trainer_card.html", context)