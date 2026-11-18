from django.db import migrations


def update_task_priorities(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")

    Task.objects.filter(priority="high").update(
        priority="medium"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_task_priorities),
    ]