from itertools import chain

from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from . import forms, models


@login_required
def flux(request):
    reviews = models.Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    mixed_posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/flux.html', context={'mixed_posts': mixed_posts})


@login_required
def posts(request):
    reviews = models.Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    mixed_posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/posts.html', context={'mixed_posts': mixed_posts})


@login_required
def subscriptions(request):
    return render(request, 'blog/subscriptions.html')


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
    return render(request, 'blog/create_ticket.html', context={'form': form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def create_review(request):
    form_ticket = forms.TicketForm()
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST)
        if all([form_ticket.is_valid(), form_review.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.closed = True
            ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('posts')

    context = {
        'form_ticket': form_ticket,
        'form_review': form_review
    }
    return render(request, 'blog/create_review.html', context=context)


@login_required
def create_review_from_ticket(request, ticket_id=None):
    existing_ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form_review = forms.ReviewForm()
    if request.method == 'POST':
        form_review = forms.ReviewForm(request.POST)
        if form_review.is_valid():
            existing_ticket.closed = True
            existing_ticket.save()
            review = form_review.save(commit=False)
            review.user = request.user
            review.ticket = existing_ticket
            review.save()
            return redirect('posts')

    context = {
        'form_review': form_review,
        'existing_ticket': existing_ticket
    }
    return render(request, 'blog/create_review_from_ticket.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, request.FILES, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.ticket.reopen()
                review.ticket.save()
                review.delete()
                return redirect('posts')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_review.html', context=context)
