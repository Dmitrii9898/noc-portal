from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("cabinet/", views.cabinet, name="cabinet"),
    path("cabinet/applications/", views.application_list, name="applications"),
    path("cabinet/applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("cabinet/applications/<int:pk>/withdraw/", views.withdraw_application, name="withdraw"),
    path("cabinet/projects/<slug:slug>/apply/", views.apply_project, name="apply_project"),
    path("cabinet/events/<slug:slug>/apply/", views.apply_event, name="apply_event"),
    path("cabinet/materials/", views.materials, name="materials"),
    path("cabinet/documents/", views.documents, name="documents"),
    path("cabinet/profile/", views.profile, name="profile"),
    path("cabinet/password/", views.UserPasswordView.as_view(), name="password"),
]
