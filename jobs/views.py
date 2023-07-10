# jobs/views.py
# from django.shortcuts import render
# from django.http import HttpResponse

### Review - this was to get articles migrations working
# from django.views.generic import ListView

# Login disabled for testing
# from django.contrib.auth.mixins import LoginRequiredMixin

# Something basic
from .models import Job
from django.http import HttpResponse

qs = Job.objects.all()
# qs = Job.objects.filter(job_name__contains="Banrock")


def jobView(request):
    # return HttpResponse(qs)
    return HttpResponse("Testing, testing")


# from .models import Action, Job


# class ActionListView(ListView):
#     model = Action
#     template_name = "action_list_view"
#     fields = ()


# class JobListView(ListView):
#     # class JobListView(LoginRequiredMixin, ListView):
#     model = Job
#     template_name = "job_list.html"


# def dashboard(request):
#     context = {"title": "Run Python logic"}
#     return render(request, "jobs/dashboard.html", context)


# def function_name(request):
#     print("\nThis is the output\n")
#     return HttpResponse(
#         """<html><script>window.location.replace('/');</script></html>"""
#     )
