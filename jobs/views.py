# jobs/views.py
# from django.shortcuts import render
# from django.http import HttpResponse

### Review - this was to get articles migrations working
# from django.views.generic import ListView

# Login disabled for testing
# from django.contrib.auth.mixins import LoginRequiredMixin

# Something basic
import json
from datetime import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, UpdateView, CreateView
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy

from jobs.forms import TaskEditForm, ActionForm, ActivityForm
from jobs.models import Job, Task, Client, Action, Activity

qs = Job.objects.all()
# qs = Job.objects.filter(job_name__contains="Banrock")


class DashboardView(TemplateView):
    """Show dashboard."""

    template_name = 'jobs/dashboard.html'

    def get_context_data(self, **kwargs):
        """Send state choices for filtering data."""
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['task_states'] = Task.STATE_CHOICES
        if self.request.GET.get('load', 'false') == 'true':
            context.update(**self.request.session.get('post_data', {}))
            if 'task_state' in context:
                context['task_state'] = int(context['task_state']) if context['task_state'] else context['task_state']
        return context


class BaseFilterMixinView(View):
    """Base class for handling filtering logic."""

    task_name = 'jobs__tasks__task_name__icontains'
    client_name = 'client_name__icontains'
    start_data_deadline = 'jobs__tasks__deadline_date__gte'
    end_date_deadline = 'jobs__tasks__deadline_date__lte'
    start_date_review = 'jobs__tasks__review_date__gte'
    end_date_review = 'jobs__tasks__review_date__gte'
    task_state = 'jobs__tasks__state'

    @staticmethod
    def format_date(date_str):
        """Change date from string to python date object."""
        return datetime.strptime(date_str, "%d/%m/%Y").date() if date_str else ''

    def get_data(self, **kwargs):
        """Get data from kwargs or POST params in request."""
        data = kwargs.get('post_data', self.request.POST)
        self.request.session['post_data'] = data
        return data

    def create_filter_data(self, data):
        """Create filter data using request parameters."""
        client_name = data['client_name']
        task_name = data['task_name']
        start_date_deadline = self.format_date(data['start_date_deadline'])
        end_date_deadline = self.format_date(data['end_date_deadline'])
        end_date_review = self.format_date(data['end_date_review'])
        start_date_review = self.format_date(data['start_date_review'])
        filter_data = {}

        # If filter data is passed for a field, add it to filter_data
        if task_name:
            filter_data[self.task_name] = task_name
        if client_name:
            filter_data[self.client_name] = client_name
        if start_date_deadline:
            filter_data[self.start_data_deadline] = start_date_deadline
        if end_date_deadline:
            filter_data[self.end_date_deadline] = end_date_deadline
        if start_date_review:
            filter_data[self.start_date_review] = start_date_review
        if end_date_review:
            filter_data[self.end_date_review] = end_date_review
        return filter_data

    def filter_task(self, data, queryset):
        """Filter based on task state."""
        task_state = data['task_state']
        if not task_state:
            return queryset

        # Exclude completed tasks if we need to see all in complete tasks
        if task_state == 'not_completed':
            return queryset.exclude(**{self.task_state: Task.COMP})
        return queryset.filter(**{self.task_state: task_state})

    def get(self, request, *args, **kwargs):
        """Retrieve post data session and render view."""
        if 'post_data' not in request.session:
            return redirect(reverse_lazy('dashboard'))
        kwargs['post_data'] = request.session['post_data']
        return self.post(request, *args, **kwargs)


class JobsTreeListView(BaseFilterMixinView):
    """Display filtered data in form of tree."""

    def post(self, request, *args, **kwargs):
        """Filter data based on filter parameters"""
        data = self.get_data(**kwargs)
        filter_data = self.create_filter_data(data)
        clients = Client.objects.prefetch_related('jobs', 'jobs__tasks', 'jobs__tasks__actions').filter(**filter_data)
        clients = list(self.filter_task(data, clients))

        # Order actions based on action order
        for client in clients:
            for job in client.jobs.all():
                for task in job.tasks.all():
                    task.ordered_actions = sorted(task.actions.all(), key=lambda action: action.action_order)
        return render(request, 'jobs/tree-results.html', context={'clients': clients})


class JobsTableListView(BaseFilterMixinView):
    """Display filtered data in form of a table."""

    task_name = 'task_name__icontains'
    client_name = 'job__client__client_name__icontains'
    start_data_deadline = 'deadline_date__gte'
    end_date_deadline = 'deadline_date__lte'
    start_date_review = 'review_date__gte'
    end_date_review = 'review_date__gte'
    task_state = 'state'

    def post(self, request, *args, **kwargs):
        """Filter data based on filter parameters"""
        data = self.get_data(**kwargs)
        filter_data = self.create_filter_data(data)
        tasks = Task.objects.select_related('job', 'job__client').filter(**filter_data).prefetch_related('actions')
        tasks = self.filter_task(data, tasks)
        return render(request, 'jobs/table-results.html', context={'tasks': tasks})


class TaskUpdateView(UpdateView):
    """View for updating a task and its actions and activities."""

    model = Task
    form_class = TaskEditForm
    template_name = 'jobs/task-update.html'
    context_object_name = 'task'

    def get_success_url(self):
        """Redirect after successful save."""
        previous_url = self.request.GET.get('previous_url')
        if previous_url:
            return previous_url
        return reverse_lazy('edit-task', kwargs={'pk': self.object.pk})


class MarkActionDoneView(View):
    """Mark list of actions as done."""

    def post(self, request, *args, **kwargs):
        """Mark actions as done based on IDs in parameters."""
        data = json.loads(request.body)
        ids = data['ids']
        Action.objects.filter(id__in=ids).update(date_done=datetime.now())
        return JsonResponse(data={}, status=200)


class EditActionView(UpdateView):
    """Edit an action."""

    model = Action
    form_class = ActionForm
    template_name = 'jobs/action-update.html'
    context_object_name = 'action'

    def get_success_url(self):
        """Redirect after successful save."""
        previous_url = self.request.GET.get('previous_url')
        if previous_url:
            return previous_url
        return reverse_lazy('edit-task', kwargs={'pk': self.object.task.id})


class EditActivityView(UpdateView):
    """Edit an activity."""

    model = Activity
    form_class = ActivityForm
    template_name = 'jobs/activity-update.html'
    context_object_name = 'activity'

    def get_success_url(self):
        """Redirect after successful save."""
        previous_url = self.request.GET.get('previous_url')
        if previous_url:
            return previous_url
        return reverse_lazy('edit-task', kwargs={'pk': self.object.task.id})


class AddActivityView(CreateView):
    """Crete a new activity for a task."""

    model = Activity
    form_class = ActivityForm
    template_name = 'jobs/activity-update.html'
    context_object_name = 'activity'

    def get_success_url(self):
        """Redirect after successful save."""
        previous_url = self.request.GET.get('previous_url')
        if previous_url:
            return previous_url
        return reverse_lazy('edit-task', kwargs={'pk': self.object.task.id})

    def get_form_kwargs(self):
        """Pass user nad task_id to creation form."""
        kwargs = super(AddActivityView, self).get_form_kwargs()
        # User defaults to 1 because authentication is not yet required,
        kwargs.update({
            'task_id': self.kwargs['task_id'],
            'user': self.request.user if self.request.user.is_authenticated else 1,
        })
        return kwargs

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
