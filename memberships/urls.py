from django.urls import path
from memberships import views
from memberships import forms

urlpatterns = [
    path("step1/", views.membership_form, name="registerstep1"),
    path("step2/<str:pk>", views.goal_form, name="registerstep2"),
    path("step3/<str:pk>", views.medicalprofile_form, name="registerstep3"),
    path("step4/<str:pk>", views.disease_form, name="registerstep4"),
    path("step5/<str:pk>", views.fee_form, name="registerstep5"),
]
