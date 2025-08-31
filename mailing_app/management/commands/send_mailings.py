from django.core.management.base import BaseCommand
from mailing_app.models import Mailing
from mailing_app.services import send_mailing

class Command(BaseCommand):
    help = 'Отправка запущенных рассылок'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='Started')
        if not mailings.exists():
            self.stdout.write('Нет активных рассылок для отправки.')
            return

        for mailing in mailings:
            self.stdout.write(f'Отправка рассылки #{mailing.pk}')
            send_mailing(mailing, from_email='your-email@example.com')
            self.stdout.write('Готово.')
