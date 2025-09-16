from django.core.mail import send_mail

from .models import MailingAttempt


def send_mailing(mailing, from_email):
    recipients = mailing.clients.all()
    subject = mailing.message.subject
    message = mailing.message.body

    for client in recipients:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = "Success"
            response = "Письмо успешно отправлено"
        except Exception as e:
            status = "Failed"
            response = str(e)
        MailingAttempt.objects.create(mailing=mailing, status=status, server_response=response)
