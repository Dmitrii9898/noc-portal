from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.mixins import admin_required, staff_required
from accounts.models import AppUser, Role
from pages.forms import NewsForm
from pages.models import Feedback, News

from .forms import EventForm, ProjectForm
from .exports import applications_csv, applications_docx, applications_xlsx
from .models import Application, AuditLog, Direction, Event, Partner, Project, Publication
from .services import ApplyError, decide, open_seats, queue_summary


@staff_required
def dashboard(request):
    request.breadcrumbs = [("Центр", None)]
    summary = queue_summary()
    return render(request, "office/dashboard.html", {
        "new_count": summary["new_total"],
        "new_events": summary["new_events"],
        "new_projects": summary["new_projects"],
        "projects": Project.objects.filter(is_open=True).count(),
        "events": Event.objects.filter(is_open=True).count(),
        "by_direction": Direction.objects.annotate(total=Count("projects")),
    })


@staff_required
def application_queue(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Заявки", None)]
    status = request.GET.get("status") or ""
    kind = request.GET.get("kind") or ""
    qs = Application.objects.select_related("user", "project", "event")
    if status:
        qs = qs.filter(status=status)
    if kind:
        qs = qs.filter(kind=kind)
    return render(request, "office/applications.html", {
        "items": qs, "status": status, "kind": kind,
    })


@staff_required
def application_decide(request, pk):
    item = get_object_or_404(Application.objects.select_related("user", "project", "event"), pk=pk)
    request.breadcrumbs = [("Центр", "/office/"), ("Заявки", "/office/applications/"), (f"Заявка {item.pk}", None)]
    if request.method == "POST":
        try:
            decide(item, request.user, approve=request.POST.get("action") == "approve", note=request.POST.get("note", ""))
        except ApplyError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Решение сохранено.")
            return redirect("center:applications")
    seats_left = open_seats(item.event) if item.event_id else None
    return render(request, "office/application_decide.html", {"item": item, "seats_left": seats_left})


@staff_required
def event_board(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Мероприятия", None)]
    items = list(Event.objects.annotate(taken=Count("applications")))
    for item in items:
        item.free = open_seats(item)
    return render(request, "office/events.html", {"items": items})


@staff_required
def event_add(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Мероприятия", "/office/events/"), ("Новое", None)]
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Мероприятие создано.")
        return redirect("center:events")
    return render(request, "office/event_form.html", {"form": form, "heading": "Новое мероприятие"})


@staff_required
def event_toggle(request, pk):
    item = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        item.is_open = not item.is_open
        item.save(update_fields=["is_open"])
        messages.success(request, "Набор на мероприятие обновлён.")
    return redirect("center:events")


@staff_required
def project_board(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Проекты", None)]
    return render(request, "office/projects.html", {"items": Project.objects.annotate(taken=Count("applications"))})


@staff_required
def project_add(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Проекты", "/office/projects/"), ("Новый", None)]
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Проект создан.")
        return redirect("center:projects")
    return render(request, "office/event_form.html", {"form": form, "heading": "Новый проект"})


@staff_required
def project_toggle(request, pk):
    item = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        item.is_open = not item.is_open
        item.save(update_fields=["is_open"])
        messages.success(request, "Набор в проект обновлён.")
    return redirect("center:projects")


@staff_required
def news_add(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Новая новость", None)]
    form = NewsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Новость опубликована.")
        return redirect("pages:news_list")
    return render(request, "office/event_form.html", {"form": form, "heading": "Новая новость"})


@staff_required
def reports(request):
    request.breadcrumbs = [("Центр", "/office/"), ("Отчёты", None)]
    items = Application.objects.select_related("user", "project", "event")
    only_new = request.GET.get("scope") == "new"
    if only_new:
        items = items.filter(status=Application.Status.NEW)
    if request.GET.get("format") == "csv":
        return applications_csv(items)
    if request.GET.get("format") == "xlsx":
        return applications_xlsx(items)
    if request.GET.get("format") == "docx":
        return applications_docx(items)
    return render(request, "office/reports.html", {"count": items.count(), "only_new": only_new})


@admin_required
def manage_home(request):
    request.breadcrumbs = [("Администрирование", None)]
    return render(request, "manage/home.html", {
        "users": AppUser.objects.count(),
        "news": News.objects.count(),
        "feedback": Feedback.objects.filter(is_processed=False).count(),
        "publications": Publication.objects.count(),
        "partners": Partner.objects.count(),
    })


@admin_required
def manage_users(request):
    request.breadcrumbs = [("Администрирование", "/office/manage/"), ("Пользователи", None)]
    if request.method == "POST":
        user = get_object_or_404(AppUser, pk=request.POST.get("user_id"))
        role = get_object_or_404(Role, pk=request.POST.get("role_id"))
        user.role = role
        user.is_staff = role.name == "Администратор"
        user.save(update_fields=["role", "is_staff"])
        messages.success(request, "Роль обновлена.")
        return redirect("center:manage_users")
    return render(request, "manage/users.html", {"items": AppUser.objects.select_related("role"), "roles": Role.objects.all()})


@admin_required
def manage_news(request):
    request.breadcrumbs = [("Администрирование", "/office/manage/"), ("Новости", None)]
    if request.method == "POST":
        item = get_object_or_404(News, pk=request.POST.get("news_id"))
        if request.POST.get("field") == "home":
            item.show_on_home = not item.show_on_home
            item.save(update_fields=["show_on_home"])
        else:
            item.is_published = not item.is_published
            item.save(update_fields=["is_published"])
        return redirect("center:manage_news")
    return render(request, "manage/news.html", {"items": News.objects.all()})


@admin_required
def manage_feedback(request):
    request.breadcrumbs = [("Администрирование", "/office/manage/"), ("Обращения", None)]
    if request.method == "POST":
        item = get_object_or_404(Feedback, pk=request.POST.get("feedback_id"))
        item.is_processed = True
        item.save(update_fields=["is_processed"])
        return redirect("center:manage_feedback")
    return render(request, "manage/feedback.html", {"items": Feedback.objects.all()})


@admin_required
def manage_publications(request):
    request.breadcrumbs = [("Администрирование", "/office/manage/"), ("Публикации", None)]
    if request.method == "POST":
        item = get_object_or_404(Publication, pk=request.POST.get("publication_id"))
        item.is_published = not item.is_published
        item.save(update_fields=["is_published"])
        return redirect("center:manage_publications")
    return render(request, "manage/publications.html", {"items": Publication.objects.all()})


@admin_required
def manage_audit(request):
    request.breadcrumbs = [("Администрирование", "/office/manage/"), ("Журнал", None)]
    return render(request, "manage/audit.html", {"items": AuditLog.objects.select_related("user")[:80]})
