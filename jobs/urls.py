"""jobs/urls.py"""

from django.urls import path
from jobs.views import (
    DashboardView, JobsTreeListView, JobsTableListView, TaskUpdateView, MarkActionDoneView, EditActionView,
    EditActivityView, AddActivityView
)

urlpatterns = [
    path('list-tree', JobsTreeListView.as_view(), name='list-tree'),
    path('list-table', JobsTableListView.as_view(), name='list-table'),
    path('task/edit/<int:pk>', TaskUpdateView.as_view(), name='edit-task'),
    path('action/mark-done', MarkActionDoneView.as_view(), name='mark-action-done'),
    path('action/edit/<int:pk>', EditActionView.as_view(), name='edit-action'),
    path('activity/edit/<int:pk>', EditActivityView.as_view(), name='edit-activity'),
    path('activity/add/<int:task_id>', AddActivityView.as_view(), name='add-activity'),
    path('', DashboardView.as_view(), name='dashboard')
]


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
