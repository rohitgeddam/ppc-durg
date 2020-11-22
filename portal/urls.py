from django.urls import path
from portal import views

urlpatterns = [
    path("members/profile/<pk>", views.memberProfileView, name="members_profile"),
    path("members/", views.MemberList.as_view(), name="members_list"),
]
