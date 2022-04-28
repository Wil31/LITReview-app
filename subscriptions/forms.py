from django import forms
from django.contrib.auth.models import User

from .models import UserFollows


class SubscriptionsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        labels = {"followed_user": ""}
        widgets = {'followed_user': forms.TextInput()}
