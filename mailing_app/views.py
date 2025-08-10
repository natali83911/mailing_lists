from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client, Message, Mailing, MailingAttempt

class ClientListView(ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:client_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing_app/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')
