# Generated by Django 4.0.10 on 2023-06-21 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0008_recur_action_recur_job_recur_task_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_comment', models.CharField(blank=True, max_length=200)),
                ('activity_date', models.DateField()),
                ('hours', models.DecimalField(decimal_places=2, max_digits=5)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
