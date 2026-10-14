"""Правила записи на мероприятия и проекты центра.

Модуль отделяет проверку мест и повторной заявки от представлений,
чтобы одно и то же правило работало и в кабинете, и в проверках.
"""
from django.db import transaction
from django.utils import timezone

from .models import Application


class ApplyError(Exception):
    """Заявку нельзя создать: мест нет или она уже подана."""


def open_seats(event):
    """Сколько мест ещё свободно на мероприятии."""
    taken = event.applications.exclude(
        status__in=(Application.Status.REJECTED, Application.Status.WITHDRAWN)
    ).count()
    return max(event.seats - taken, 0)


def already_applied(user, project=None, event=None):
    """Повторная активная заявка того же участника на тот же объект."""
    qs = Application.objects.filter(user=user).exclude(
        status__in=(Application.Status.REJECTED, Application.Status.WITHDRAWN)
    )
    if project is not None:
        return qs.filter(project=project).exists()
    return qs.filter(event=event).exists()


def can_apply(user, project=None, event=None):
    """Возвращает текст причины отказа или пустую строку, если заявка допустима."""
    if project is not None:
        if not project.is_open:
            return "Набор в проект закрыт."
        if already_applied(user, project=project):
            return "Заявка в этот проект уже подана."
        return ""
    if event is None:
        return "Не выбран проект или мероприятие."
    if not event.is_open:
        return "Запись на мероприятие закрыта."
    if open_seats(event) <= 0:
        return "Свободных мест не осталось."
    if already_applied(user, event=event):
        return "Заявка на это мероприятие уже подана."
    return ""


@transaction.atomic
def submit_application(user, comment, attachment, project=None, event=None):
    """Создаёт заявку, если правила записи это позволяют."""
    reason = can_apply(user, project=project, event=event)
    if reason:
        raise ApplyError(reason)
    item = Application(
        user=user,
        kind=Application.Kind.PROJECT if project is not None else Application.Kind.EVENT,
        project=project,
        event=event,
        comment=comment or "",
        status=Application.Status.NEW,
    )
    if attachment:
        item.attachment = attachment
    item.save()
    return item


@transaction.atomic
def decide(application, actor, approve, note=""):
    """Фиксирует решение сотрудника, комментарий и время решения."""
    if application.status != Application.Status.NEW:
        raise ApplyError("Решение уже принято.")
    if approve and application.event_id and open_seats(application.event) <= 0:
        raise ApplyError("Свободных мест не осталось.")
    application.status = Application.Status.APPROVED if approve else Application.Status.REJECTED
    application.decision_note = (note or "")[:300]
    application.decided_at = timezone.now()
    application.decided_by = actor
    application.save(update_fields=["status", "decision_note", "decided_at", "decided_by"])
    return application


@transaction.atomic
def withdraw(application, user):
    """Участник отзывает только свою ещё не рассмотренную заявку."""
    if application.user_id != user.id:
        raise ApplyError("Можно отозвать только свою заявку.")
    if application.status != Application.Status.NEW:
        raise ApplyError("Отозвать можно только новую заявку.")
    application.status = Application.Status.WITHDRAWN
    application.save(update_fields=["status"])
    return application


def queue_summary():
    """Сводка очереди для панели сотрудника."""
    new_items = Application.objects.filter(status=Application.Status.NEW)
    return {
        "new_total": new_items.count(),
        "new_events": new_items.filter(kind=Application.Kind.EVENT).count(),
        "new_projects": new_items.filter(kind=Application.Kind.PROJECT).count(),
    }
