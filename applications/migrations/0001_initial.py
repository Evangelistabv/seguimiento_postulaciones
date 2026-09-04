from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="JobApplication", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=180, verbose_name="puesto")),
            ("company", models.CharField(blank=True, max_length=140, verbose_name="empresa")),
            ("vacancy_url", models.URLField(blank=True, verbose_name="enlace de la vacante")),
            ("source", models.CharField(blank=True, max_length=80, verbose_name="fuente")),
            ("status", models.CharField(choices=[("saved", "Guardada"), ("applied", "Postulación enviada"), ("screening", "Entrevista RR. HH."), ("technical", "Entrevista técnica"), ("offer", "Oferta recibida"), ("accepted", "Oferta aceptada"), ("rejected", "Rechazada"), ("withdrawn", "Retirada"), ("closed", "Vacante cerrada")], default="saved", max_length=20, verbose_name="estado")),
            ("location", models.CharField(blank=True, max_length=120, verbose_name="ubicación")),
            ("work_mode", models.CharField(choices=[("remote", "Remoto"), ("hybrid", "Híbrido"), ("onsite", "Presencial"), ("unknown", "Sin especificar")], default="unknown", max_length=12, verbose_name="modalidad")),
            ("salary_min", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="salario mínimo")),
            ("salary_max", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="salario máximo")),
            ("currency", models.CharField(blank=True, default="MXN", max_length=8, verbose_name="moneda")),
            ("salary_period", models.CharField(blank=True, default="mensual", max_length=30, verbose_name="periodicidad")),
            ("applied_on", models.DateField(blank=True, null=True, verbose_name="fecha de postulación")),
            ("next_step_on", models.DateField(blank=True, null=True, verbose_name="próximo seguimiento")),
            ("priority", models.PositiveSmallIntegerField(choices=[(1, "Alta"), (2, "Media"), (3, "Baja")], default=2, verbose_name="prioridad")),
            ("responsibilities", models.TextField(blank=True, help_text="Actividades, entregables y expectativas descritas en la vacante.", verbose_name="responsabilidades de la vacante")),
            ("requirements", models.TextField(blank=True, verbose_name="requisitos clave")),
            ("notes", models.TextField(blank=True, verbose_name="notas")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
        ], options={"ordering": ["priority", "-updated_at"]}),
        migrations.CreateModel(name="Activity", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("kind", models.CharField(choices=[("note", "Nota"), ("follow_up", "Seguimiento"), ("interview", "Entrevista"), ("task", "Tarea"), ("status", "Cambio de estado")], default="note", max_length=20, verbose_name="tipo")),
            ("title", models.CharField(max_length=160, verbose_name="actividad")),
            ("details", models.TextField(blank=True, verbose_name="detalle")),
            ("scheduled_for", models.DateTimeField(blank=True, null=True, verbose_name="fecha programada")),
            ("completed", models.BooleanField(default=False, verbose_name="completada")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("application", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activities", to="applications.jobapplication")),
        ], options={"ordering": ["completed", "-scheduled_for", "-created_at"]}),
    ]
