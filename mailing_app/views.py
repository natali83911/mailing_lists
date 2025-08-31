from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView

from .form import MailingForm, ClientForm, MessageForm
from .models import Client, Message, Mailing, MailingAttempt
from .services import send_mailing

class ClientListView(ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
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
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailing_app/mailingattempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_id = self.request.GET.get('mailing')
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)
        return queryset

class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing, from_email='your-email@example.com')
        messages.success(request, f'Рассылка #{mailing.pk} успешно отправлена!')
        return redirect('mailing_app:mailing_list')

class HomeView(TemplateView):
    template_name = 'mailing_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Started').count()
        context['unique_clients'] = Client.objects.filter(mailing__status='Started').distinct().count()
        return context