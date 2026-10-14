from django.contrib import admin

from .models import Application, AuditLog, CenterDocument, Direction, Event, Partner, Project, Publication

admin.site.register(Direction)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(Application)
admin.site.register(Publication)
admin.site.register(Partner)
admin.site.register(CenterDocument)
admin.site.register(AuditLog)
