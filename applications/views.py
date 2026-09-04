from datetime import timedelta
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import ActivityForm, ApplicationForm
from .models import Activity, JobApplication


ACTIVE_STATUSES = [
    JobApplication.Status.SAVED, JobApplication.Status.APPLIED,
    JobApplication.Status.SCREENING, JobApplication.Status.TECHNICAL,
    JobApplication.Status.OFFER,
]


def dashboard(request):
    today = timezone.localdate()
    applications = JobApplication.objects.all()
    active = applications.filter(status__in=ACTIVE_STATUSES)
    upcoming = Activity.objects.filter(completed=False, scheduled_for__date__gte=today).select_related("application").order_by("scheduled_for")[:6]
    overdue = Activity.objects.filter(completed=False, scheduled_for__date__lt=today).select_related("application").order_by("scheduled_for")
    recent = applications[:6]
    funnel = applications.values("status").annotate(total=Count("id"))
    return render(request, "applications/dashboard.html", {
        "active_count": active.count(),
        "total_count": applications.count(),
        "interview_count": active.filter(status__in=[JobApplication.Status.SCREENING, JobApplication.Status.TECHNICAL]).count(),
        "offer_count": applications.filter(status__in=[JobApplication.Status.OFFER, JobApplication.Status.ACCEPTED]).count(),
        "upcoming": upcoming, "overdue": overdue, "recent": recent, "funnel": funnel,
    })


def application_list(request):
    applications = JobApplication.objects.all()
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    if query:
        applications = applications.filter(Q(title__icontains=query) | Q(company__icontains=query) | Q(source__icontains=query))
    if status:
        applications = applications.filter(status=status)
    return render(request, "applications/application_list.html", {"applications": applications, "query": query, "status": status, "statuses": JobApplication.Status.choices})


def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    form = ActivityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        activity = form.save(commit=False)
        activity.application = application
        activity.save()
        messages.success(request, "Actividad registrada.")
        return redirect(application)
    return render(request, "applications/application_detail.html", {"application": application, "activity_form": form})


def application_create(request):
    form = ApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save()
        messages.success(request, "Postulación creada.")
        return redirect(application)
    return render(request, "applications/application_form.html", {"form": form, "title": "Nueva postulación"})


def application_update(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    form = ApplicationForm(request.POST or None, instance=application)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cambios guardados.")
        return redirect(application)
    return render(request, "applications/application_form.html", {"form": form, "title": "Editar postulación", "application": application})


def toggle_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.completed = not activity.completed
        activity.save(update_fields=["completed"])
    return redirect(activity.application)
