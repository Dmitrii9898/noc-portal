"""Предметная область портала Научно-образовательного центра."""
from django.conf import settings
from django.db import models
from django.urls import reverse


class Direction(models.Model):
    """Направление работы центра, соотнесённое с целью устойчивого развития."""

    code = models.CharField("Код ЦУР", max_length=8)
    title = models.CharField("Наименование", max_length=160)
    slug = models.SlugField("Ссылка", max_length=80, unique=True)
    summary = models.CharField("Кратко", max_length=300)
    body = models.TextField("Описание")

    class Meta:
        db_table = "direction"
        ordering = ["code"]
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

    def __str__(self):
        return f"{self.code} {self.title}"

    def get_absolute_url(self):
        return reverse("pages:direction_detail", args=[self.slug])


class Project(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="projects", verbose_name="Направление")
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(max_length=120, unique=True)
    summary = models.CharField("Анонс", max_length=300)
    body = models.TextField("Описание")
    started_on = models.DateField("Начало")
    is_open = models.BooleanField("Набор открыт", default=True)

    class Meta:
        db_table = "project"
        ordering = ["-started_on"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:project_detail", args=[self.slug])


class Event(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="events", verbose_name="Направление")
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(max_length=120, unique=True)
    place = models.CharField("Место", max_length=160)
    starts_at = models.DateTimeField("Начало")
    summary = models.CharField("Анонс", max_length=300)
    body = models.TextField("Описание")
    seats = models.PositiveIntegerField("Мест", default=40)
    is_open = models.BooleanField("Запись открыта", default=True)

    class Meta:
        db_table = "event"
        ordering = ["starts_at"]
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:event_detail", args=[self.slug])


class Application(models.Model):
    """Заявка участника на проект или мероприятие."""

    class Kind(models.TextChoices):
        PROJECT = "project", "Проект"
        EVENT = "event", "Мероприятие"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        APPROVED = "approved", "Принята"
        REJECTED = "rejected", "Отклонена"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    kind = models.CharField("Тип", max_length=16, choices=Kind.choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="applications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name="applications")
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.NEW)
    comment = models.TextField("Комментарий", blank=True)
    attachment = models.FileField("Файл", upload_to="applications/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="decided_applications"
    )

    class Meta:
        db_table = "application"
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        target = self.project or self.event
        return f"{self.user} — {target}"


class Publication(models.Model):
    title = models.CharField("Название", max_length=240)
    authors = models.CharField("Авторы", max_length=240)
    year = models.PositiveIntegerField("Год")
    summary = models.CharField("Аннотация", max_length=400)
    file = models.FileField("Файл", upload_to="publications/", blank=True)
    is_published = models.BooleanField("На портале", default=True)

    class Meta:
        db_table = "publication"
        ordering = ["-year", "title"]
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField("Наименование", max_length=180)
    kind = models.CharField("Тип", max_length=80)
    site = models.URLField("Сайт", blank=True)
    description = models.TextField("О партнёре")

    class Meta:
        db_table = "partner"
        ordering = ["name"]
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class CenterDocument(models.Model):
    title = models.CharField("Наименование", max_length=200)
    file = models.FileField("Файл", upload_to="documents/")
    published_on = models.DateField("Дата")

    class Meta:
        db_table = "center_document"
        ordering = ["-published_on"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_entries")
    action = models.CharField(max_length=200)
    entity = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]
        verbose_name = "Запись журнала"
        verbose_name_plural = "Журнал"

    def __str__(self):
        return self.action
