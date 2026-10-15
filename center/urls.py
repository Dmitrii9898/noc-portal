from django.urls import path

from . import views

app_name = "center"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("applications/", views.application_queue, name="applications"),
    path("applications/<int:pk>/", views.application_decide, name="application_decide"),
    path("events/", views.event_board, name="events"),
    path("events/new/", views.event_add, name="event_add"),
    path("events/<int:pk>/toggle/", views.event_toggle, name="event_toggle"),
    path("projects/", views.project_board, name="projects"),
    path("projects/new/", views.project_add, name="project_add"),
    path("projects/<int:pk>/toggle/", views.project_toggle, name="project_toggle"),
    path("news/new/", views.news_add, name="news_add"),
    path("reports/", views.reports, name="reports"),
    path("manage/", views.manage_home, name="manage_home"),
    path("manage/directions/<int:pk>/", views.manage_direction, name="manage_direction"),
    path("manage/users/", views.manage_users, name="manage_users"),
    path("manage/partners/new/", views.manage_partner_add, name="manage_partner_add"),
    path("manage/news/", views.manage_news, name="manage_news"),
    path("manage/feedback/", views.manage_feedback, name="manage_feedback"),
    path("manage/publications/", views.manage_publications, name="manage_publications"),
    path("manage/audit/", views.manage_audit, name="manage_audit"),
]
