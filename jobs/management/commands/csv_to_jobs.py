# jobs/management/commands/add_test_data.py
"""This must be run from python manage.py, from within Admin in Django
    or from an external call (not sure how).
    It cannot be run from a normal Python file (security??)
    
    The csv file ***MUST*** be in the same folder as manage.py
    and the data must be structured so that a value in a cell triggers a new record"""

from django.core.management.base import BaseCommand, CommandError


# import importlib
import csv


def do_import():
    file_name = "./jobs_etc.csv"
    client_pk = job_ok = task_pk = action_pk = 0
    new_jobs = new_tasks = new_actions = 0

    with open(file_name, newline="") as csvfile:
        result = ""
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Client_id"]:
                client_pk = row["Client_id"]
            if row["Job"]:
                job = row["Job"]
                # new_rec = Job(client_id=1, job_name=job)
                # new_rec.save()
                # job_pk = new_rec.id
                # new_jobs += 1
            if row["Task"]:
                task = row["Task"]
            #     new_rec = Task(job_id=job_pk, task_name=task)
            #     new_rec.save()
            #     task_pk = new_rec.id
            #     new_tasks += 1
            if row["Action"]:
                action = row["Action"]
            #     new_rec = Action(task_id=task_pk, action_name=action)
            #     new_rec.save()
            #     new_actions += 1
            break
    result = f"values are: {client_pk}, {job}, {task}, {action}"
    # result = f"Processing completed - records added:- {new_jobs} jobs, {new_tasks} tasks, {new_actions} actions "
    return result


class Command(BaseCommand):
    help = "Test adding a record to client table using Django management"

    from jobs.models import Client, Job, Task, Action

    def handle(self, *args, **options):
        try:
            # returned = do_import()
            new_rec = Job(job_name="Job name")  # lient_id=1,
            new_rec.save()

            # self.stdout.write(self.style.SUCCESS(returned))

        except:
            raise CommandError("Something went wrong")

        self.stdout.write(self.style.SUCCESS(f"The process has ended "))
