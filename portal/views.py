from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

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

from attendance.models import MemberAttendance

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
    MemberClassificationForm,
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


def convert_seconds_to_hours(seconds):
    # return format(seconds * 0.000277778, ".2f")
    return format(seconds / (60 * 60), ".2f")


def convert_seconds_to_minutes(seconds):
    return format(seconds / 60, ".2f")


def calculate_total_workout_time(all_days):
    # calculate total workout
    total_workout_seconds = 0.0
    for day in all_days:
        try:
            diff = day.out_time - day.in_time
            total_workout_seconds = total_workout_seconds + diff.seconds
        except:
            continue

    return (
        convert_seconds_to_minutes(total_workout_seconds),
        convert_seconds_to_hours(total_workout_seconds),
    )


@login_required
def memberProfileView(request, pk):
    member = Member.objects.filter(pk=pk).first()
    all_days = MemberAttendance.objects.filter(member=member)

    total_days_present = all_days.count()

    total_workout_minutes, total_workout_hours = calculate_total_workout_time(all_days)

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
        "total_workout_hours": total_workout_hours,
        "total_workout_minutes": total_workout_minutes,
        "total_workout_days": total_days_present,
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
    last_fee = member.fee.last()

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
        # print(fee.date_of_payment, fee.amount_paid)
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


@login_required
def fee_stats(request):
    return render(request, "portal/fee/stats.html")


def calculate_revenue_in_range(request):
    from_date = request.GET.get("from_date", None)
    to_date = request.GET.get("to_date", None)

    try:
        paid_fee_in_range = Fee.objects.filter(
            date_of_payment__gte=from_date, date_of_payment__lte=to_date
        )
    except:
        pass

    if from_date and to_date:

        if from_date > to_date:
            data = {"message": "From Date must be before To Date"}
        else:
            sum = 0
            for fee in paid_fee_in_range:
                sum = sum + fee.amount_paid

            data = {
                "from_date": from_date,
                "to_date": to_date,
                "message": "success",
                "revenue": sum,
            }

    else:
        data = {"message": "Please Input Dates"}

    return JsonResponse(data)


def get_attendance_stats(request, pk):
    member = Member.objects.filter(pk=pk).first()
    from_date = request.GET.get("from_date", None)
    to_date = request.GET.get("to_date", None)

    attendance_in_range = MemberAttendance.objects.filter(
        member__pk=pk, sheet__date__gte=from_date, sheet__date__lte=to_date
    )

    from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d")

    to_date_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d")

    total_days_in_range = (to_date_obj - from_date_obj).days + 1

    days_present_count = attendance_in_range.count()

    (
        total_workout_minutes_in_range,
        total_workout_hours_in_range,
    ) = calculate_total_workout_time(attendance_in_range)

    if from_date and to_date:
        if from_date_obj > to_date_obj:
            data = {"message": "From Date must be before To Date"}
        else:
            data = {
                "from_date": from_date,
                "to_date": to_date,
                "total_days_in_range": total_days_in_range,
                "total_days_present_in_range": days_present_count,
                "total_workout_hours_in_range": total_workout_hours_in_range,
                "total_workout_minutes_in_range": total_workout_minutes_in_range,
                "message": "success",
            }
    else:
        data = {"message": "Please provide From Date and To Date"}

    return JsonResponse(data)


def member_stats(request):
    active_members = Member.objects.filter(is_active=True)
    all_members = Member.objects.all()
    form = MemberClassificationForm()
    # print(active_members)
    context = {
        "active_members": active_members,
        "all_members": all_members,
        "form": form,
    }
    return render(request, "portal/members/stats.html", context)


def member_stats_search(request):
    member_classification = request.GET.get("member_classification", None)
    # membership_duration = reques.GET.get("membership-duration", None)
    # print(member_classification)
    member_list = Member.objects.filter(
        membership_classification=member_classification,
    )
    # print(member_list)

    id_list = []
    pk_list = []
    members_name_list = []

    for member in member_list:
        pk_list.append(member.pk)
        members_name_list.append(member.first_name + member.last_name)
        id_list.append(member.membership_id)

    if len(id_list) > 0:
        data = {
            "id_list": id_list,
            "members_name_list": members_name_list,
            "pk_list": pk_list,
            "message": "success",
        }
    else:
        data = {
            "id_list": id_list,
            "members_name_list": members_name_list,
            "pk_list": pk_list,
            "message": "No records found",
        }

    return JsonResponse(data)
