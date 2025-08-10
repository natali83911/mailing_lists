from django.db import models

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = (
        ('Created', 'Создана'),
        ('Started', 'Запущена'),
        ('Finished', 'Завершена'),
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f'Отправка #{self.pk} - {self.status}'

class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ('Success', 'Успешно'),
        ('Failed', 'Не успешно'),
    )

    attempt_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f'Попытка #{self.pk} отправки по почте #{self.mailing.pk} - {self.status}'

