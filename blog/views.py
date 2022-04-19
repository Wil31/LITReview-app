from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from . import forms, models


@login_required
def flux(request):
    return render(request, 'blog/flux.html')


@login_required
def posts(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/posts.html', context={'tickets': tickets})


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
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
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
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('flux')
            if 'delete_ticket' in request.POST:
                delete_form = forms.DeleteTicketForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect('flux')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def create_review(request):
    return render(request, 'blog/create_review.html')
