from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
)

app_name = "mailing_app"


urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/form/', ClientUpdateView.as_view(), name='client_form'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_confirm_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/add/', MessageCreateView.as_view(), name='message_add'),
    path('messages/<int:pk>/form/', MessageUpdateView.as_view(), name='message_form'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_confirm_delete'),
]
