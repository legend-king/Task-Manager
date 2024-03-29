# Generated by Django 4.2.10 on 2024-02-11 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_options_task_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='sub_tasks',
        ),
        migrations.RemoveField(
            model_name='taskcategory',
            name='sub_categories',
        ),
        migrations.AddField(
            model_name='task',
            name='sub_task_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
        migrations.AddField(
            model_name='taskcategory',
            name='sub_category_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.taskcategory'),
        ),
    ]
