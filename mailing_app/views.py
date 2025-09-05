from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView

from config.settings import EMAIL_HOST_USER
from .forms import MailingForm, ClientForm, MessageForm
from .models import Client, Message, Mailing, MailingAttempt
from .services import send_mailing

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing_app/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing_app/mailingattempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_id = self.request.GET.get('mailing')
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)
        return queryset

class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing, from_email=EMAIL_HOST_USER)
        messages.success(request, f'Рассылка #{mailing.pk} успешно отправлена!')
        return redirect('mailing_app:mailing_list')


class MailingToggleActiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Менеджеры').exists()

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()
        messages.success(request, f"Рассылка #{mailing.pk} теперь {'активна' if mailing.is_active else 'отключена'}.")
        return redirect('mailing_app:mailing_list')


class HomeView(TemplateView):
    template_name = 'mailing_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Started').count()
        context['unique_clients'] = Client.objects.filter(mailing__status='Started').distinct().count()
        return context





