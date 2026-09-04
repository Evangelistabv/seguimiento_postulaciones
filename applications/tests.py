from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Activity, JobApplication


class ApplicationFlowTests(TestCase):
    def setUp(self):
        self.application = JobApplication.objects.create(title="Backend Developer", company="Acme", status="applied")

    def test_dashboard_and_list_render(self):
        self.assertEqual(self.client.get(reverse("applications:dashboard")).status_code, 200)
        response = self.client.get(reverse("applications:list"), {"q": "Backend"})
        self.assertContains(response, "Backend Developer")
        self.assertEqual(self.client.get(self.application.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(reverse("applications:update", args=[self.application.pk])).status_code, 200)

    def test_create_application(self):
        response = self.client.post(reverse("applications:create"), {"title": "DevOps Engineer", "status": "saved", "priority": 1, "work_mode": "remote"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobApplication.objects.filter(title="DevOps Engineer").exists())

    def test_add_and_complete_activity(self):
        response = self.client.post(self.application.get_absolute_url(), {"kind": "follow_up", "title": "Escribir a reclutamiento"})
        activity = Activity.objects.get(application=self.application)
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse("applications:toggle_activity", args=[activity.pk]))
        activity.refresh_from_db()
        self.assertTrue(activity.completed)
