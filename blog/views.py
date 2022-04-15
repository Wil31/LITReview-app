from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def flux(request):
    return render(request, 'blog/flux.html')


@login_required
def posts(request):
    return render(request, 'blog/posts.html')


@login_required
def subscriptions(request):
    return render(request, 'blog/subscriptions.html')


@login_required
def create_ticket(request):
    return render(request, 'blog/create_ticket.html')


@login_required
def create_review(request):
    return render(request, 'blog/create_review.html')
