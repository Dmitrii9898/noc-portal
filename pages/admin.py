from django.contrib import admin

from .models import Feedback, News

admin.site.register(News)
admin.site.register(Feedback)
