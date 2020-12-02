from django.urls import path
from portal import views

urlpatterns = [
    path("members/stats", views.member_stats, name="member_stats"),
    path("members/stats/search", views.member_stats_search, name="member_stats_search"),
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
    path(
        "members/<pk>/stats/attendance",
        views.get_attendance_stats,
        name="get_attendance_stats",
    ),
    path("members/profile/<pk>", views.memberProfileView, name="members_profile"),
    path("members/", views.MemberList.as_view(), name="members_list"),
    path("trainers/", views.TrainerList.as_view(), name="trainers_list"),
    path("pendingfees/", views.PendingFeeList.as_view(), name="pending_fee_list"),
    path(
        "fees/stats/calculate/",
        views.calculate_revenue_in_range,
        name="calculate_revenue",
    ),
    path("fees/", views.FeeList.as_view(), name="fee_list"),
    path("fees/stats/", views.fee_stats, name="fee_stats"),
    path("fees/pay/<pk>", views.PayFee, name="pay_fee"),
    path("card/<pk>/print", views.print_card, name="card_print"),
    path(
        "card/trainer/<pk>/print", views.print_trainer_card, name="card_trainer_print"
    ),
    path("fees/<str:fee_id>/print", views.print_fee_recipt, name="fee_print"),
    path("", views.DashboardView, name="dashboard"),
]
