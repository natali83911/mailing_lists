from django.db import models

from config import settings


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        null=False,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("can_view_all", "Can view all records for managers"),
        ]


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        null=False,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.subject

    class Meta:
        permissions = [
            ("can_view_all", "Can view all records for managers"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = (
        ("Created", "Создана"),
        ("Started", "Запущена"),
        ("Finished", "Завершена"),
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        null=False,
        blank=True,
        verbose_name="Владелец",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Отправка #{self.pk} - {self.status}"

    class Meta:
        permissions = [
            ("can_view_all", "Can view all records for managers"),
            ("can_send_mailing", "Can send mailing"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ("Success", "Успешно"),
        ("Failed", "Не успешно"),
    )

    attempt_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"Попытка #{self.pk} отправки по почте #{self.mailing.pk} - {self.status}"
        )

    class Meta:
        permissions = [
            ("can_view_all", "Can view all records for managers"),
        ]
