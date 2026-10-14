from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render

from center.forms import ApplicationForm
from center.models import Application, Event, Project
from center.services import ApplyError, can_apply, submit_application

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import ROLE_MEMBER, Role


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        request.breadcrumbs = [("Вход", None)]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_admin_role:
            return "/office/manage/"
        if user.is_staff_role:
            return "/office/"
        return "/accounts/cabinet/"


class UserLogoutView(LogoutView):
    next_page = "pages:home"


def register(request):
    request.breadcrumbs = [("Регистрация", None)]
    if request.user.is_authenticated:
        return redirect("accounts:cabinet")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.full_name = form.cleaned_data["full_name"]
        user.organization = form.cleaned_data["organization"]
        user.role, _created = Role.objects.get_or_create(name=ROLE_MEMBER, defaults={"description": "Подаёт заявки и видит свои материалы"})
        user.save()
        login(request, user)
        messages.success(request, "Учётная запись создана.")
        return redirect("accounts:cabinet")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def cabinet(request):
    request.breadcrumbs = [("Личный кабинет", None)]
    apps = Application.objects.filter(user=request.user).select_related("project", "event")
    return render(request, "accounts/cabinet.html", {"applications": apps})


@login_required
def application_list(request):
    request.breadcrumbs = [("Личный кабинет", "/accounts/cabinet/"), ("Мои заявки", None)]
    items = Application.objects.filter(user=request.user).select_related("project", "event")
    return render(request, "accounts/applications.html", {"items": items})


@login_required
def apply_project(request, slug):
    project = get_object_or_404(Project, slug=slug, is_open=True)
    request.breadcrumbs = [("Проекты", "/projects/"), (project.title, project.get_absolute_url()), ("Заявка", None)]
    return _apply(request, project=project)


@login_required
def apply_event(request, slug):
    event = get_object_or_404(Event, slug=slug, is_open=True)
    request.breadcrumbs = [("Мероприятия", "/events/"), (event.title, event.get_absolute_url()), ("Заявка", None)]
    return _apply(request, event=event)


def _apply(request, project=None, event=None):
    form = ApplicationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        try:
            submit_application(
                request.user,
                form.cleaned_data.get("comment"),
                form.cleaned_data.get("attachment"),
                project=project,
                event=event,
            )
        except ApplyError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Заявка отправлена в центр.")
            return redirect("accounts:applications")
    title = project.title if project else event.title
    block_reason = can_apply(request.user, project=project, event=event)
    return render(request, "accounts/apply.html", {"form": form, "title": title, "block_reason": block_reason})


@login_required
def materials(request):
    request.breadcrumbs = [("Личный кабинет", "/accounts/cabinet/"), ("Материалы", None)]
    from center.models import Publication
    return render(request, "accounts/materials.html", {"items": Publication.objects.filter(is_published=True)[:12]})


@login_required
def documents(request):
    request.breadcrumbs = [("Личный кабинет", "/accounts/cabinet/"), ("Мои файлы", None)]
    files = Application.objects.filter(user=request.user).exclude(attachment="")
    return render(request, "accounts/documents.html", {"files": files})


@login_required
def profile(request):
    request.breadcrumbs = [("Личный кабинет", "/accounts/cabinet/"), ("Профиль", None)]
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль сохранён.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
