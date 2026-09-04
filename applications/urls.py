from django.urls import path
from . import views

app_name = "applications"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("postulaciones/", views.application_list, name="list"),
    path("postulaciones/nueva/", views.application_create, name="create"),
    path("postulaciones/<int:pk>/", views.application_detail, name="detail"),
    path("postulaciones/<int:pk>/editar/", views.application_update, name="update"),
    path("actividades/<int:pk>/alternar/", views.toggle_activity, name="toggle_activity"),
]
