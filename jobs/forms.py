from django import forms
from django.core.exceptions import ValidationError

from jobs.models import Task, Action, Activity


class ActionForm(forms.ModelForm):
    """Form to edit and action."""

    class Meta:
        model = Action
        fields = ['action_comment']


class ActivityForm(forms.ModelForm):
    """Form to create or edit an activity."""

    class Meta:
        model = Activity
        fields = ['activity_comment', 'hours', ]

    def __init__(self, task_id=None, user=None, *args, **kwargs):
        """Get task_id and user from view."""
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.task_id = task_id
        self.user = user

    def save(self, commit=True):
        """Attach task_id and user from view to instance of activity."""
        activity = super(ActivityForm, self).save(commit=False)

        # Set the task and user for the activity
        if self.task_id:
            activity.task_id = self.task_id
        if self.user:
            activity.user = self.user

        if commit:
            activity.save()
        return activity


class TaskEditForm(forms.ModelForm):
    """Form used to edit a task."""

    class Meta:
        model = Task
        fields = ['id', 'deadline_date', 'review_date', 'state', 'task_description']

    def __init__(self, *args, **kwargs):
        """Check if state of a task is completed or not:

        if completed, disable changing state
        if not completed, remove completed from state choices
        """
        super(TaskEditForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        if instance:
            if instance.state == Task.COMP:
                self.fields['state'].widget.attrs['disabled'] = True
            else:
                self.fields['state'].choices = [
                    (choice[0], choice[1]) for choice in self.fields['state'].choices if choice[0] != Task.COMP
                ]

    def clean(self):
        """Clean data for form."""
        cleaned_data = super().clean()
        instance = self.instance

        # if there is not state in data, use the old state
        if not cleaned_data['state']:
            cleaned_data['state'] = instance.state
        new_state = cleaned_data.get('state')

        # Check if the state is being changed to "Completed"
        if new_state == Task.COMP and instance.state != Task.COMP:
            raise ValidationError("You cannot change the state to 'Completed'.")

        # Check if the state is being changed from "Completed"
        if new_state != Task.COMP and instance.state == Task.COMP:
            raise ValidationError("You cannot change the state from 'Completed'.")

        return cleaned_data
