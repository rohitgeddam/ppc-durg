from django.shortcuts import render
from django.views.generic import ListView
from memberships.models import Member

# Create your views here.
class MemberList(ListView):
    model = Member
    template_name = "portal/members/list.html"
    context_object_name = "members_list"
    paginate_by = 20