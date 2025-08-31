from django.urls import path
from .views import (
    HomeView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingAttemptListView,
    MailingSendView,
)

app_name = "mailing_app"


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/form/', ClientUpdateView.as_view(), name='client_form'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_confirm_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/add/', MessageCreateView.as_view(), name='message_add'),
    path('messages/<int:pk>/form/', MessageUpdateView.as_view(), name='message_form'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_confirm_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/add/', MailingCreateView.as_view(), name='mailing_add'),
    path('mailings/<int:pk>/form/', MailingUpdateView.as_view(), name='mailing_form'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),

    path('attempts/', MailingAttemptListView.as_view(), name='mailingattempt_list'),
]
