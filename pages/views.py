from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from center.models import Direction, Event, Partner, Project, Publication
from center.services import open_seats

from .forms import FeedbackForm
from .models import News


def home(request):
    request.breadcrumbs = []
    return render(request, "pages/home.html", {
        "directions": Direction.objects.all()[:4],
        "events": Event.objects.filter(is_open=True)[:3],
        "projects": Project.objects.filter(is_open=True)[:3],
        "news": News.objects.filter(is_published=True, show_on_home=True)[:3],
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
    opened = request.GET.get("open") == "1"
    direction = request.GET.get("direction") or ""
    qs = Project.objects.select_related("direction")
    if opened:
        qs = qs.filter(is_open=True)
    if direction:
        qs = qs.filter(direction__slug=direction)
    return render(request, "pages/projects.html", {
        "items": qs, "opened": opened, "directions": Direction.objects.all(), "direction": direction,
    })


def project_detail(request, slug):
    item = get_object_or_404(Project.objects.select_related("direction"), slug=slug)
    request.breadcrumbs = [("Проекты", "/projects/"), (item.title, None)]
    return render(request, "pages/project_detail.html", {"item": item})


def event_list(request):
    request.breadcrumbs = [("Мероприятия", None)]
    when = request.GET.get("when", "upcoming")
    direction = request.GET.get("direction") or ""
    qs = Event.objects.select_related("direction")
    if when == "past":
        qs = qs.filter(starts_at__lt=timezone.now())
    else:
        when = "upcoming"
        qs = qs.filter(starts_at__gte=timezone.now())
    if direction:
        qs = qs.filter(direction__slug=direction)
    return render(request, "pages/events.html", {
        "items": qs, "when": when, "directions": Direction.objects.all(), "direction": direction,
    })


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
    year = request.GET.get("year") or ""
    qs = Publication.objects.filter(is_published=True)
    years = qs.values_list("year", flat=True).distinct().order_by("-year")
    if year.isdigit():
        qs = qs.filter(year=int(year))
    return render(request, "pages/publications.html", {"items": qs, "years": years, "year": year})


def partners(request):
    request.breadcrumbs = [("Партнёры", None)]
    return render(request, "pages/partners.html", {"items": Partner.objects.order_by("kind", "name")})


def partner_detail(request, pk):
    item = get_object_or_404(Partner, pk=pk)
    request.breadcrumbs = [("Партнёры", "/partners/"), (item.name, None)]
    return render(request, "pages/partner_detail.html", {"item": item})


def documents(request):
    request.breadcrumbs = [("Документы", None)]
    from center.models import CenterDocument
    return render(request, "pages/documents.html", {"items": CenterDocument.objects.all()})


def faq(request):
    request.breadcrumbs = [("Вопросы и ответы", None)]
    return render(request, "pages/faq.html")


def glossary(request):
    request.breadcrumbs = [("Глоссарий", None)]
    terms = [
        ("ЦУР 4", "Качественное образование: доступ к знаниям об устойчивом развитии."),
        ("ЦУР 11", "Устойчивые города и населённые пункты."),
        ("ЦУР 12", "Ответственное потребление и производство."),
        ("ЦУР 13", "Борьба с изменением климата и учёт климатических рисков."),
        ("НОЦ", "Научно-образовательный центр устойчивого развития университета."),
    ]
    return render(request, "pages/glossary.html", {"terms": terms})


def help_page(request):
    request.breadcrumbs = [("Справка", None)]
    return render(request, "pages/help.html")


def sitemap_page(request):
    request.breadcrumbs = [("Карта портала", None)]
    return render(request, "pages/sitemap.html")


def search(request):
    request.breadcrumbs = [("Поиск", None)]
    query = (request.GET.get("q") or "").strip()
    projects = events = news = []
    if query:
        projects = Project.objects.filter(title__icontains=query)
        events = Event.objects.filter(title__icontains=query)
        news = News.objects.filter(is_published=True, title__icontains=query)
    return render(request, "pages/search.html", {
        "query": query, "projects": projects, "events": events, "news": news,
    })


def contacts(request):
    request.breadcrumbs = [("Контакты", None)]
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Сообщение отправлено в центр.")
        return redirect("pages:contacts")
    return render(request, "pages/contacts.html", {"form": form})
