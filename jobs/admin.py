# jobs/admin.py
from django.contrib import admin

from .models import Action
from .models import Activity
from .models import Client

# from .models import Default_action
# from .models import Default_task
# from .models import Defaults_map
from .models import Job
from .models import Recur_action
from .models import Recur_job
from .models import Recur_task
from .models import Settings
from .models import Task

admin.site.register(Action)
admin.site.register(Activity)
admin.site.register(Client)
# admin.site.register(Default_action)
# admin.site.register(Default_task)
# admin.site.register(Defaults_map)
admin.site.register(Job)
admin.site.register(Recur_action)
admin.site.register(Recur_job)
admin.site.register(Recur_task)
admin.site.register(Settings)


admin.site.register(Task)
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = (
#         "client__client_name",
#         "job__job_name",
#         "task_name",
#         "task_description",
#     )
