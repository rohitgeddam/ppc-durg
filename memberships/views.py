from django.shortcuts import render
from memberships import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from memberships import models
from django.contrib.auth.decorators import login_required
from datetime import date

# from django.template.loader import render_to_string
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from weasyprint import HTML

# Create your views here.
@login_required
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


@login_required
def trainer_form(request):

    if request.method == "POST":
        form = forms.TrainerForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.save()
            # return HttpResponseRedirect(
            #     reverse("registerstep2", args=[form.instance.pk])
            # )
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        form = forms.TrainerForm()
    return render(request, "memberships/trainer_register.html", {"form": form})


@login_required
def goal_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = forms.GoalFormSet(
            request.POST,
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            member.registeration_step = 3
            member.save()
            for form in formset:

                if form.cleaned_data != {}:
                    try:
                        form.save(commit=False)
                        form.instance.member = member
                        form.save()
                    except:
                        continue

            return HttpResponseRedirect(reverse("registerstep3", args=[pk]))
            # return render(request, "memberships/registeration_done.html")
    else:
        formset = forms.GoalFormSet()
    return render(
        request,
        "memberships/registeration_step2.html",
        {"form": formset, "member_id": pk},
    )


@login_required
def medicalprofile_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = forms.MedicalProfileForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            member.registeration_step = 4
            member.save()
            form.save(commit=False)
            form.instance.member = member
            form.save()
            return HttpResponseRedirect(reverse("registerstep4", args=[pk]))

    else:
        form = forms.MedicalProfileForm()
    return render(
        request, "memberships/registeration_step3.html", {"form": form, "member_id": pk}
    )


@login_required
def disease_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = forms.DiseaseFormset(
            request.POST,
            queryset=models.Disease.objects.none(),
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            member.registeration_step = 5
            member.save()
            for form in formset:
                # form.save(commit=False)
                if form.cleaned_data != {}:
                    try:
                        form.instance.member = member
                        form.save()
                    except:
                        continue

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


@login_required
def fee_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = forms.FeeForm(request.POST)
        if form.is_valid():
            member.registeration_step = 0
            member.is_active = True
            member.is_registeration_done = True
            member.save()
            # do something with the formset.cleaned_data

            form.save(commit=False)
            form.instance.initial_date = date.today()
            form.instance.member = member
            form.save()
            return HttpResponseRedirect(reverse("members_profile", args=[pk]))

    else:
        form = forms.FeeForm()
    return render(
        request, "memberships/registeration_step5.html", {"form": form, "member_id": pk}
    )


# def done_pdf(request, pk):
#     member = models.Members.objects.get(pk=pk)
#     context = {"member": member}
#     html_string = render_to_string(
#         "memberships/registeration_done.html", {"context": context}
#     )

#     html = HTML(string=html_string)
#     html.write_pdf(target="/tmp/mypdf.pdf")

#     fs = FileSystemStorage("/tmp")
#     with fs.open("mypdf.pdf") as pdf:
#         response = HttpResponse(pdf, content_type="application/pdf")
#         response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
#         return response

#     return response