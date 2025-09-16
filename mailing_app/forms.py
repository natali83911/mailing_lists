from django import forms
from django.forms import BooleanField, ImageField

from .models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "checkbox-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "checkbox-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_datetime", "end_datetime", "status", "message", "clients"]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "checkbox-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_datetime")
        end = cleaned_data.get("end_datetime")

        if start and end and start >= end:
            raise forms.ValidationError("Дата и время начала должны быть раньше даты и времени окончания.")

        return cleaned_data


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            elif isinstance(fild, ImageField):
                fild.widget.attrs["class"] = "form-control-file"
            else:
                fild.widget.attrs["class"] = "form-control"
