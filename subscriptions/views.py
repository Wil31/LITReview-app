from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from . import forms, models


@login_required
def subscriptions(request):
    users = User.objects.all()
    user_follows = models.UserFollows.objects.all()
    subscribers = request.user.followed_by.all()
    if request.method == 'POST':
        entry = request.POST['followed_user']
        user_to_follow = User.objects.get(username=entry)
        for user in users:
            if user.username == entry:
                models.UserFollows.objects.create(user=request.user,
                                                  followed_user=user_to_follow)
        return redirect('subscriptions')
    else:
        form = forms.SubscriptionsForm()

    context = {
        'form': form,
        'current_user': request.user,
        'subscribers': subscribers,
        'user_follows': user_follows
    }
    return render(request, 'subscriptions/subscriptions.html', context=context)


class SubscriptionDeleteView(LoginRequiredMixin,
                             DeleteView,
                             SuccessMessageMixin
                             ):
    model = models.UserFollows
    success_url = reverse_lazy('subscriptions')
    success_message = "Abonnement résilié"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = User.objects.get(id=self.request.user.id)
        context['followed_user'] = models.UserFollows.objects.exclude(
            user=current_user)
        return context
