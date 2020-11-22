from django.urls import path
from portal import views

urlpatterns = [
    path(
        "members/profile/details/update/<pk>",
        views.MemberDetailsUpdate.as_view(),
        name="member_details_update",
    ),
    path(
        "members/<int:memberId>/profile/goals/update/<pk>",
        views.GoalUpdateView.as_view(),
        name="member_goals_update",
    ),
    path(
        "members/<int:memberId>/profile/medicalprofile/update/<pk>",
        views.MedicalProfileUpdateView.as_view(),
        name="member_medical_profile_update",
    ),
    path(
        "members/<pk>/profile/goal/create",
        views.goalCreateView,
        name="member_goal_create",
    ),
    path(
        "members/<pk>/profile/disease/create",
        views.diseaseAddView,
        name="member_disease_create",
    ),
    path(
        "members/<pk>/generalexam/create",
        views.GeneralExamCreateView,
        name="member_general_exam_create",
    ),
    path(
        "members/<pk>/systemicexam/create",
        views.SystemicExamCreateView,
        name="member_systemic_exam_create",
    ),
    path("members/profile/<pk>", views.memberProfileView, name="members_profile"),
    path("members/", views.MemberList.as_view(), name="members_list"),
]
