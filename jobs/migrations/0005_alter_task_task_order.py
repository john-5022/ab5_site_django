# Generated by Django 4.0.10 on 2023-03-31 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_task_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_order',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
