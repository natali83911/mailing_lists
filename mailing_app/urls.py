from django.contrib import admin
from mailing_app.apps import MailingAppConfig

app_name = MailingAppConfig.name

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path("", include("mailing_app.urls", namespace="mailing_app"))
]