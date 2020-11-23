from django.urls import path
from attendance import views

urlpatterns = [
    path("members/<pk>/attend", views.MemberSetInTime, name="member_attend"),
    path("members/<pk>/attend/out", views.MemberSetOutTime, name="member_attend_out"),
    path("members/", views.MemberList.as_view(), name="member_attendance_list"),
    path("trainers/", views.TrainerList.as_view(), name="trainer_attendance_list"),
    path("trainers/<pk>/attend", views.TrainerSetInTime, name="trainer_attend"),
    path(
        "trainers/<pk>/attend/out", views.TrainerSetOutTime, name="trainer_attend_out"
    ),
]
