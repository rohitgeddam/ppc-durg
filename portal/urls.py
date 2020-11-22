from django.urls import path
from portal import views

urlpatterns = [
    path("members/", views.MemberList.as_view(), name="members_list"),
]
