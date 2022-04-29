from django import forms

from .models import UserFollows


class SubscriptionsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
        labels = {"followed_user": ""}
        widgets = {"followed_user": forms.TextInput()}
