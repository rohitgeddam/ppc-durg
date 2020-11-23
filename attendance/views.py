from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, CreateView
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from memberships.models import Member, Trainer
from attendance.models import AttendanceSheet, MemberAttendance, TrainerAttendance

import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone

# Create your views here.
class MemberList(ListView):
    model = Member
    template_name = "portal/attendance/member_list.html"
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


def MemberSetInTime(request, pk):
    sheet = AttendanceSheet.objects.filter(date=datetime.date.today()).first()
    member = Member.objects.filter(pk=pk).first()
    if not sheet:
        # create a new sheet
        sheet = AttendanceSheet(date=datetime.date.today())
        sheet.save()

    try:
        attendance = MemberAttendance(sheet=sheet, member=member)

        attendance.save()
    except:
        print("already attended")

    return HttpResponseRedirect(reverse_lazy("member_attendance_list"))


def MemberSetOutTime(request, pk):
    sheet = AttendanceSheet.objects.filter(date=datetime.date.today()).first()
    member = Member.objects.filter(pk=pk).first()
    if not sheet:
        # create a new sheet
        sheet = AttendanceSheet(date=datetime.date.today())
        sheet.save()

    try:
        attendance = MemberAttendance.objects.get(sheet=sheet, member=member)
        attendance.out_time = timezone.now()
        attendance.save()
    except:
        print("Member not in")

    return HttpResponseRedirect(reverse_lazy("member_attendance_list"))


class TrainerList(ListView):
    model = Trainer
    template_name = "portal/attendance/trainer_list.html"
    context_object_name = "trainers_list"
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
            )
        else:
            object_list = self.model.objects.all()
        return object_list


def TrainerSetInTime(request, pk):
    sheet = AttendanceSheet.objects.filter(date=datetime.date.today()).first()
    trainer = Trainer.objects.filter(pk=pk).first()
    if not sheet:
        # create a new sheet
        sheet = AttendanceSheet(date=datetime.date.today())
        sheet.save()

    try:
        attendance = TrainerAttendance(sheet=sheet, trainer=trainer)

        attendance.save()
    except:
        print("already attended")

    return HttpResponseRedirect(reverse_lazy("trainer_attendance_list"))


def TrainerSetOutTime(request, pk):
    sheet = AttendanceSheet.objects.filter(date=datetime.date.today()).first()
    trainer = Trainer.objects.filter(pk=pk).first()
    if not sheet:
        # create a new sheet
        sheet = AttendanceSheet(date=datetime.date.today())
        sheet.save()

    try:
        attendance = TrainerAttendance.objects.get(sheet=sheet, trainer=trainer)
        attendance.out_time = timezone.now()
        attendance.save()
    except:
        print("Member not in")

    return HttpResponseRedirect(reverse_lazy("trainer_attendance_list"))
