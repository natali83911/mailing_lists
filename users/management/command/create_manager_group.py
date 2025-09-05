from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing_app.models import Client, Mailing
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает группу Менеджеры с нужными правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Менеджеры')

        client_ct = ContentType.objects.get_for_model(Client)
        mailing_ct = ContentType.objects.get_for_model(Mailing)
        user_ct = ContentType.objects.get_for_model(User)

        permissions = [
            Permission.objects.get(codename='view_client', content_type=client_ct),
            Permission.objects.get(codename='view_mailing', content_type=mailing_ct),
            Permission.objects.get(codename='view_user', content_type=user_ct),
            Permission.objects.get(codename='change_user', content_type=user_ct),
        ]
        for perm in permissions:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана и права назначены'))
