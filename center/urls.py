from django.urls import path

from . import views

app_name = "center"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("applications/", views.application_queue, name="applications"),
    path("applications/<int:pk>/", views.application_decide, name="application_decide"),
    path("events/", views.event_board, name="events"),
    path("events/<int:pk>/toggle/", views.event_toggle, name="event_toggle"),
    path("projects/", views.project_board, name="projects"),
    path("reports/", views.reports, name="reports"),
    path("manage/", views.manage_home, name="manage_home"),
    path("manage/users/", views.manage_users, name="manage_users"),
    path("manage/news/", views.manage_news, name="manage_news"),
    path("manage/feedback/", views.manage_feedback, name="manage_feedback"),
    path("manage/publications/", views.manage_publications, name="manage_publications"),
    path("manage/audit/", views.manage_audit, name="manage_audit"),
]
