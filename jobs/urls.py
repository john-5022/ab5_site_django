# jobs/urls.py

from django.urls import path
from .views import jobView

urlpatterns = [path("jobs", jobView, name="job_list")]


# from django.contrib import admin
# from django.urls import path
# from .views import (
#     ActionListView,
#     JobListView,
# )

# ### Review - this was to get articles migrations working


# urlpatterns = [
#     path("jobs", JobListView.as_view(), name="job_list"),
# ]
