from django import forms

from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "Titre du livre",
                  "description": "Description",
                  "image": "Image"
                  }


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "Titre de la critique",
                  "rating": "Note",
                  "body": "Commentaire"
                  }
        CHOICES = [(0, '0'),
                   (1, '1'),
                   (2, '2'),
                   (4, '3'),
                   (4, '4'),
                   (5, '5')
                   ]
        widgets = {"rating": forms.RadioSelect(choices=CHOICES),
                   "body": forms.Textarea()
                   }


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
