from django.urls import path

from . import views

app_name = "pages"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("directions/", views.direction_list, name="direction_list"),
    path("directions/<slug:slug>/", views.direction_detail, name="direction_detail"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("events/", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("news/", views.news_list, name="news_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("publications/", views.publications, name="publications"),
    path("partners/", views.partners, name="partners"),
    path("documents/", views.documents, name="documents"),
    path("faq/", views.faq, name="faq"),
    path("help/", views.help_page, name="help"),
    path("contacts/", views.contacts, name="contacts"),
]
