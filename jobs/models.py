# jobs/models.py
from django.conf import settings
from django.db import models


# Create action table - action_description is static - action_comment is for users
class Action(models.Model):
    action_comment = models.CharField(max_length=200, blank=True, help_text="For users")
    action_description = models.CharField(
        max_length=200, blank=True, help_text="Normally from default"
    )
    action_name = models.CharField(
        max_length=25, blank=False, help_text="Normally from default"
    )
    action_order = models.IntegerField(
        blank=False, default=0, help_text="Normally from default"
    )
    date_done = models.DateField(
        blank=True, null=True, help_text="Set by system when user marks as done"
    )
    task = models.ForeignKey("Task", related_name='actions', on_delete=models.CASCADE)

    def __str__(self):
        return self.action_name


# Create activity table - activity_comment is for users
class Activity(models.Model):
    activity_comment = models.CharField(max_length=200, blank=True)  # For users
    activity_date = models.DateField(auto_now_add=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    task = models.ForeignKey("Task", related_name='activities', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )  # Do not delete users - make inactive

    def __str__(self) -> str:
        return self.activity_comment

    class Meta:
        verbose_name_plural = "Activities"


# Create the client table
class Client(models.Model):
    client_code = models.CharField(max_length=10, unique=True, blank=False)
    client_name = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.client_name


# # Create default_action table - _comment changed to _description
# class Default_action(models.Model):
#     d_action_description = models.CharField(max_length=200, blank=True)
#     d_action_name = models.CharField(max_length=50, blank=False)

#     def __str__(self):
#         return self.d_action_name

# # Create the default_task table - _comment changed to _description
# class Default_task(models.Model):
#     d_task_description = models.CharField(max_length=35, blank=False)
#     d_task_name = models.CharField(max_length=35, blank=False)

#     def __str__(self):
#         return self.d_task_name

# # Create the defaults_map table
# # This defines the order of default actions for a default task
# #ToDo review
# class Defaults_map(models.Model):
#     d_action_id = models.IntegerField(blank=False)
#     d_action_order = models.IntegerField(blank=False)
#     d_task_id = models.IntegerField(blank=False)


# Create the job table
class Job(models.Model):
    client = models.ForeignKey("Client", related_name='jobs', on_delete=models.CASCADE)
    folder_url = models.CharField(max_length=100, blank=True)
    job_name = models.CharField(max_length=100, blank=False)
    period_end = models.DateField(blank=True)

    def __str__(self):
        return self.job_name


# Create the recur_action table
class Recur_action(models.Model):
    r_action_description = models.CharField(max_length=100, blank=True)
    r_action_name = models.CharField(max_length=80, blank=False)
    r_action_order = models.IntegerField(blank=True)
    recur_task = models.ForeignKey("Recur_task", on_delete=models.CASCADE)

    def __str__(self):
        return self.r_action_name

    class Meta:
        verbose_name_plural = "Recurring Actions"


# # Create the recur_job table
class Recur_job(models.Model):
    FREQUENCIES = [
        ("day", "day"),
        ("month", "month"),
        ("week", "week"),
    ]
    JOB_NAMES = [
        ("EOM", "EOM"),
        ("EOQ", "EOQ"),
        ("Pays", "Pays"),
    ]
    build_delay = models.IntegerField(
        default=0, blank=False, help_text="Days before / after next_period_end"
    )
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    every = models.IntegerField(blank=False, help_text="Paired with period_freq")
    fin_year = models.IntegerField(blank=False, help_text="Is this needed?")
    # fold_client_url = models.CharField(max_length=120, blank=False)
    # fold_year_url = models.CharField(max_length=120, blank=False)
    job_name_start = models.CharField(max_length=4, choices=JOB_NAMES, blank=False)
    next_build_date = models.DateField(blank=False, help_text="Normally calculated")
    next_period_end = models.DateField(blank=False, help_text="Normally calculated")
    period_freq = models.CharField(max_length=5, choices=FREQUENCIES, blank=False)

    def __str__(self):
        return (
            f"{self.job_name_start} {self.next_period_end} - {self.client.client_name}"
        )

    class Meta:
        verbose_name_plural = "Recurring Jobs"


# Create the recur_task table
class Recur_task(models.Model):
    eofy = models.BooleanField(blank=False, default=False)
    eom = models.BooleanField(blank=False, default=False)
    eom_ex_eoq = models.BooleanField(blank=False, default=False)
    eoq = models.BooleanField(blank=False, default=False)
    recur_job = models.ForeignKey("Recur_job", on_delete=models.CASCADE)
    # r_state_id = models.IntegerField(default=1, blank=False)
    r_task_description = models.CharField(max_length=100, blank=True)
    r_task_name = models.CharField(max_length=50, blank=False)
    r_task_order = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.r_task_name} {self.recur_job.job_name_start} {self.recur_job.client.client_name}"

    class Meta:
        verbose_name_plural = "Recurring Tasks"


# Create the settings table ToDo is this needed?
class Settings(models.Model):
    end_fin_year = models.DateField(blank=False)


# class State(models.Model):
#     filter_default = models.IntegerField(default=0)
#     is_completed = models.IntegerField(default=0)
#     is_default = models.IntegerField(default=0)
#     not_completed = models.IntegerField(default=0)
#     state_description = models.CharField(max_length=80, blank=True)
#     state_name = models.CharField(max_length=30, blank=False)


# Create the task table - _comment changed to _description
# Choices are subclassed to ensure data integrity.
# ...The first part is not used, 2nd is stored in db,
# ...3rd is displayed - set field length to fit this text.
class Task(models.Model):
    ACT = 1
    AWOK = 2
    AWIN = 3
    COMP = 4
    FUP = 5
    INP = 6
    LOD = 7
    TOI = 8

    STATE_CHOICES = {
        'Action needed': ACT,
        'Await OK to lodge...': AWOK,
        'Await information': AWIN,
        'Completed': COMP,
        'Follow up': FUP,
        'In progress': INP,
        'Lodged - ATO to file': LOD,
        'To invoice something': TOI,
    }

    deadline_date = models.DateField(blank=True, null=False, help_text="Set as needed")
    job = models.ForeignKey("Job", related_name='tasks', on_delete=models.CASCADE)
    review_date = models.DateField(blank=True, null=True, help_text="Set as needed")
    state = models.PositiveSmallIntegerField(
        choices=[(value, key) for key, value in STATE_CHOICES.items()], null=True, blank=True
    )
    task_description = models.CharField(max_length=100, blank=True, default=None)
    task_name = models.CharField(max_length=80, blank=False)
    task_order = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.task_name
