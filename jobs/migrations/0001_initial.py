# Generated by Django 4.0.10 on 2023-03-30 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_code', models.CharField(max_length=10, unique=True)),
                ('client_name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Default_action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_action_description', models.CharField(blank=True, max_length=200)),
                ('d_action_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Default_task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_task_description', models.CharField(max_length=35)),
                ('d_task_name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Defaults_map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_action_id', models.IntegerField()),
                ('d_action_order', models.IntegerField()),
                ('d_task_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_url', models.CharField(blank=True, max_length=100)),
                ('job_name', models.CharField(max_length=100)),
                ('period_end', models.DateField(blank=True)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.client')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_fin_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline_date', models.DateField(blank=True)),
                ('review_date', models.DateField(blank=True)),
                ('state_id', models.IntegerField(default=1)),
                ('task_description', models.CharField(blank=True, max_length=100)),
                ('task_name', models.CharField(max_length=80)),
                ('task_order', models.IntegerField(blank=True)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_comment', models.CharField(blank=True, max_length=200)),
                ('action_description', models.CharField(blank=True, max_length=200)),
                ('action_name', models.CharField(max_length=25)),
                ('action_order', models.IntegerField(blank=True)),
                ('date_done', models.DateField(blank=True)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.task')),
            ],
        ),
    ]
