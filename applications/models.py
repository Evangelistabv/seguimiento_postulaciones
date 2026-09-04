from django.db import models
from django.urls import reverse


class JobApplication(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Guardada"
        APPLIED = "applied", "Postulación enviada"
        SCREENING = "screening", "Entrevista RR. HH."
        TECHNICAL = "technical", "Entrevista técnica"
        OFFER = "offer", "Oferta recibida"
        ACCEPTED = "accepted", "Oferta aceptada"
        REJECTED = "rejected", "Rechazada"
        WITHDRAWN = "withdrawn", "Retirada"
        CLOSED = "closed", "Vacante cerrada"

    class WorkMode(models.TextChoices):
        REMOTE = "remote", "Remoto"
        HYBRID = "hybrid", "Híbrido"
        ONSITE = "onsite", "Presencial"
        UNKNOWN = "unknown", "Sin especificar"

    title = models.CharField("puesto", max_length=180)
    company = models.CharField("empresa", max_length=140, blank=True)
    vacancy_url = models.URLField("enlace de la vacante", blank=True)
    source = models.CharField("fuente", max_length=80, blank=True)
    status = models.CharField("estado", max_length=20, choices=Status.choices, default=Status.SAVED)
    location = models.CharField("ubicación", max_length=120, blank=True)
    work_mode = models.CharField("modalidad", max_length=12, choices=WorkMode.choices, default=WorkMode.UNKNOWN)
    salary_min = models.DecimalField("salario mínimo", max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField("salario máximo", max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField("moneda", max_length=8, default="MXN", blank=True)
    salary_period = models.CharField("periodicidad", max_length=30, default="mensual", blank=True)
    applied_on = models.DateField("fecha de postulación", null=True, blank=True)
    next_step_on = models.DateField("próximo seguimiento", null=True, blank=True)
    priority = models.PositiveSmallIntegerField("prioridad", default=2, choices=[(1, "Alta"), (2, "Media"), (3, "Baja")])
    responsibilities = models.TextField("responsabilidades de la vacante", blank=True, help_text="Actividades, entregables y expectativas descritas en la vacante.")
    requirements = models.TextField("requisitos clave", blank=True)
    notes = models.TextField("notas", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "-updated_at"]

    def __str__(self):
        return f"{self.title} · {self.company or 'Empresa pendiente'}"

    def get_absolute_url(self):
        return reverse("applications:detail", args=[self.pk])

    @property
    def salary_display(self):
        if self.salary_min is None and self.salary_max is None:
            return "No especificado"
        values = [v for v in (self.salary_min, self.salary_max) if v is not None]
        amount = " – ".join(f"{v:,.0f}" for v in values)
        return f"{self.currency} ${amount} / {self.salary_period}"


class Activity(models.Model):
    class Kind(models.TextChoices):
        NOTE = "note", "Nota"
        FOLLOW_UP = "follow_up", "Seguimiento"
        INTERVIEW = "interview", "Entrevista"
        TASK = "task", "Tarea"
        STATUS = "status", "Cambio de estado"

    application = models.ForeignKey(JobApplication, related_name="activities", on_delete=models.CASCADE)
    kind = models.CharField("tipo", max_length=20, choices=Kind.choices, default=Kind.NOTE)
    title = models.CharField("actividad", max_length=160)
    details = models.TextField("detalle", blank=True)
    scheduled_for = models.DateTimeField("fecha programada", null=True, blank=True)
    completed = models.BooleanField("completada", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["completed", "-scheduled_for", "-created_at"]

    def __str__(self):
        return self.title
