from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages

from . import forms, models


@login_required
def subscriptions(request):
    current_user = request.user
    users = User.objects.all()
    user_follows = models.UserFollows.objects.all()
    subscribers = current_user.followed_by.all()
    if request.method == 'POST':
        entry = request.POST['followed_user']

        if entry == current_user.username:
            messages.warning(request, "You cannot follow yourself !")
            return redirect('subscriptions')

        for user in user_follows:
            if user.followed_user.username == entry:
                messages.warning(request,
                               f"You already follow : {user.followed_user.username}")
                return redirect('subscriptions')

        for user in users:
            if user.username == entry:
                user_to_follow = User.objects.get(username=entry)
                models.UserFollows.objects.create(user=current_user,
                                                  followed_user=user_to_follow)
                messages.success(request,
                                 f"New followed user : {user_to_follow.username}")
                return redirect('subscriptions')

        messages.warning(request, f"User {entry} does not exist !")
        return redirect('subscriptions')

    else:
        form = forms.SubscriptionsForm()

    context = {
        'form': form,
        'current_user': current_user,
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
