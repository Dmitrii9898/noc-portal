from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from center.models import Direction, Event, Partner, Project, Publication
from center.services import open_seats

from .forms import FeedbackForm
from .models import News


def home(request):
    request.breadcrumbs = []
    return render(request, "pages/home.html", {
        "directions": Direction.objects.all()[:4],
        "events": Event.objects.filter(is_open=True)[:3],
        "news": News.objects.filter(is_published=True)[:3],
    })


def about(request):
    request.breadcrumbs = [("О центре", None)]
    return render(request, "pages/about.html")


def direction_list(request):
    request.breadcrumbs = [("Направления", None)]
    return render(request, "pages/directions.html", {"items": Direction.objects.all()})


def direction_detail(request, slug):
    item = get_object_or_404(Direction, slug=slug)
    request.breadcrumbs = [("Направления", "/directions/"), (item.title, None)]
    return render(request, "pages/direction_detail.html", {"item": item, "projects": item.projects.all()})


def project_list(request):
    request.breadcrumbs = [("Проекты", None)]
    return render(request, "pages/projects.html", {"items": Project.objects.select_related("direction")})


def project_detail(request, slug):
    item = get_object_or_404(Project.objects.select_related("direction"), slug=slug)
    request.breadcrumbs = [("Проекты", "/projects/"), (item.title, None)]
    return render(request, "pages/project_detail.html", {"item": item})


def event_list(request):
    request.breadcrumbs = [("Мероприятия", None)]
    return render(request, "pages/events.html", {"items": Event.objects.select_related("direction")})


def event_detail(request, slug):
    item = get_object_or_404(Event.objects.select_related("direction"), slug=slug)
    request.breadcrumbs = [("Мероприятия", "/events/"), (item.title, None)]
    return render(request, "pages/event_detail.html", {"item": item, "seats_left": open_seats(item)})


def news_list(request):
    request.breadcrumbs = [("Новости", None)]
    return render(request, "pages/news_list.html", {"items": News.objects.filter(is_published=True)})


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, is_published=True)
    request.breadcrumbs = [("Новости", "/news/"), (item.title, None)]
    return render(request, "pages/news_detail.html", {"item": item})


def publications(request):
    request.breadcrumbs = [("Публикации", None)]
    return render(request, "pages/publications.html", {"items": Publication.objects.filter(is_published=True)})


def partners(request):
    request.breadcrumbs = [("Партнёры", None)]
    return render(request, "pages/partners.html", {"items": Partner.objects.all()})


def documents(request):
    request.breadcrumbs = [("Документы", None)]
    from center.models import CenterDocument
    return render(request, "pages/documents.html", {"items": CenterDocument.objects.all()})


def faq(request):
    request.breadcrumbs = [("Вопросы и ответы", None)]
    return render(request, "pages/faq.html")


def help_page(request):
    request.breadcrumbs = [("Справка", None)]
    return render(request, "pages/help.html")


def contacts(request):
    request.breadcrumbs = [("Контакты", None)]
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Сообщение отправлено в центр.")
        return redirect("pages:contacts")
    return render(request, "pages/contacts.html", {"form": form})
