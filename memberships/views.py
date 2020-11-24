from django.shortcuts import render
from memberships import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from memberships import models

# Create your views here.
def membership_form(request):

    if request.method == "POST":
        form = forms.MemberForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.instance.registeration_step = 2
            form.save()
            return HttpResponseRedirect(
                reverse("registerstep2", args=[form.instance.pk])
            )

    else:
        form = forms.MemberForm()
    return render(request, "memberships/registeration_step1.html", {"form": form})


def trainer_form(request):

    if request.method == "POST":
        form = forms.TrainerForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.save()
            # return HttpResponseRedirect(
            #     reverse("registerstep2", args=[form.instance.pk])
            # )
            return render(request, "memberships/registeration_done.html")

    else:
        form = forms.TrainerForm()
    return render(request, "memberships/trainer_register.html", {"form": form})


def goal_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = forms.GoalFormSet(
            request.POST,
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            for form in formset:

                if form.cleaned_data != {}:
                    form.instance.registeration_step = 3
                    form.save(commit=False)
                    form.instance.member = member
                    form.save()

            return HttpResponseRedirect(reverse("registerstep3", args=[pk]))
            # return render(request, "memberships/registeration_done.html")
    else:
        formset = forms.GoalFormSet()
    return render(
        request,
        "memberships/registeration_step2.html",
        {"form": formset, "member_id": pk},
    )


def medicalprofile_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = forms.MedicalProfileForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.instance.registeration_step = 4
            form.save(commit=False)
            form.instance.member = member
            form.save()
            return HttpResponseRedirect(reverse("registerstep4", args=[pk]))

    else:
        form = forms.MedicalProfileForm()
    return render(
        request, "memberships/registeration_step3.html", {"form": form, "member_id": pk}
    )


def disease_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = forms.DiseaseFormset(
            request.POST,
            queryset=models.Disease.objects.none(),
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            form.instance.registeration_step = 5
            for form in formset:
                # form.save(commit=False)
                if form.cleaned_data != {}:
                    form.instance.member = member
                    form.save()

            return HttpResponseRedirect(reverse("registerstep5", args=[pk]))
            # return render(request, "memberships/registeration_step5.html")
    else:
        formset = forms.DiseaseFormset(
            queryset=models.Disease.objects.none(),
        )
    return render(
        request,
        "memberships/registeration_step4.html",
        {"form": formset, "member_id": pk},
    )


def fee_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = forms.FeeForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.instance.registeration_step = 0
            form.instance.is_registeration_done = True
            form.save(commit=False)
            form.instance.member = member
            form.save()
            return HttpResponseRedirect(reverse("members_profile", args=[pk]))
            # return render(request, "memberships/registeration_done.html")

    else:
        form = forms.FeeForm()
    return render(
        request, "memberships/registeration_step5.html", {"form": form, "member_id": pk}
    )