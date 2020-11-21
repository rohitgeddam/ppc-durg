from django.urls import path
from memberships import views
from memberships import forms

urlpatterns = [
    path("register/step1/", views.membership_form, name="registerstep1"),
    path("register/step2/<str:pk>", views.goal_form, name="registerstep2"),
]
