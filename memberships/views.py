from django.shortcuts import render
from memberships import forms

# Create your views here.
def membership_form(request):

    if request.method == "POST":
        form = forms.MemberForm(request.POST)
        if form.is_valid():
            # do something with the formset.cleaned_data
            form.save()
    else:
        form = forms.MemberForm()
    return render(request, "memberships/member_form.html", {"form": form})
