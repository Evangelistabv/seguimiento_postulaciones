from django.db import migrations


def seed(apps, schema_editor):
    JobApplication = apps.get_model("applications", "JobApplication")
    JobApplication.objects.get_or_create(
        title="Junior DevOps / Cloud Engineer",
        defaults={"source": "LinkedIn", "status": "applied", "salary_min": 20000, "currency": "MXN", "salary_period": "mensual"},
    )


class Migration(migrations.Migration):
    dependencies = [("applications", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
