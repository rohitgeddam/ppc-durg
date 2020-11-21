from django.urls import path
from memberships import views
from memberships import forms

urlpatterns = [
    path("register/step1/", views.membership_form, name="registerstep1"),
    path("register/step2/<str:pk>", views.goal_form, name="registerstep2"),
    path("register/step3/<str:pk>", views.medicalprofile_form, name="registerstep3"),
    path("register/step4/<str:pk>", views.disease_form, name="registerstep4"),
    path("register/step5/<str:pk>", views.fee_form, name="registerstep5"),
]
