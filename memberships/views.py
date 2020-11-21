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
            form.save()
            return HttpResponseRedirect(
                reverse("registerstep2", args=[form.instance.pk])
            )

    else:
        form = forms.MemberForm()
    return render(request, "memberships/registeration_step1.html", {"form": form})


def goal_form(request, pk):
    member = models.Member.objects.filter(pk=pk).first()
    if request.method == "POST":
        formset = forms.GoalFormSet(
            request.POST,
            queryset=models.Goal.objects.none(),
        )
        if formset.is_valid():
            # do something with the formset.cleaned_data
            for form in formset:
                form.save(commit=False)
                form.instance.member = member
                form.save()

            # return HttpResponseRedirect(reverse("registerstep2", args=[pk]))
            return render(request, "memberships/registeration_done.html")
    else:
        formset = forms.GoalFormSet(
            queryset=models.Goal.objects.none(),
        )
    return render(
        request,
        "memberships/registeration_step2.html",
        {"form": formset, "member_id": pk},
    )
