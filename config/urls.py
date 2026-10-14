from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "НОЦ «Устойчивое развитие»"
admin.site.site_title = "НОЦ"
admin.site.index_title = "Панель администратора"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("office/", include("center.urls")),
    path("", include("pages.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
