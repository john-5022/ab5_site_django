# Generated by Django 4.0.10 on 2023-03-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_alter_task_task_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='action',
            name='date_done',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_date',
            field=models.DateField(blank=True),
        ),
    ]