from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField("Анонс", max_length=300)
    body = models.TextField("Текст")
    published_at = models.DateTimeField("Дата")
    is_published = models.BooleanField(default=True)

    class Meta:
        db_table = "news"
        ordering = ["-published_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:news_detail", args=[self.slug])


class Feedback(models.Model):
    name = models.CharField("Имя", max_length=120)
    email = models.EmailField("Эл. почта")
    subject = models.CharField("Тема", max_length=160)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField("Обработано", default=False)

    class Meta:
        db_table = "feedback"
        ordering = ["-created_at"]
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"

    def __str__(self):
        return self.subject
