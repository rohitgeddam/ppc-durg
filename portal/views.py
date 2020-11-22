from django.shortcuts import render
from django.views.generic import ListView
from memberships.models import Member
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

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