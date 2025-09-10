from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Создает Менеджера с нужными правами"

    def handle(self, *args, **options):
        email = "manager1@example.com"
        password = "123"
        user = CustomUser.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        user.is_staff = False
        users_group, created = Group.objects.get_or_create(name="Менеджер")
        user.groups.add(users_group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Пользователь добавлен в группу "Менеджер"\n' f"email для входа: {email}\n" f"пароль: {password}"
            )
        )
