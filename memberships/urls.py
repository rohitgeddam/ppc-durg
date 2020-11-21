from django.urls import path
from memberships import views

urlpatterns = [path("register/", views.membership_form, name="register")]
