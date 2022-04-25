"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordChangeDoneView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/landing.html',
        redirect_authenticated_user=True,
    ), name='landing'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('flux/', blog.views.flux, name='flux'),
    path('posts/', blog.views.posts, name='posts'),
    path('subscriptions/', blog.views.subscriptions, name='subscriptions'),
    path('create_ticket/', blog.views.create_ticket, name='create_ticket'),
    path('create_review/', blog.views.create_review, name='create_review'),
    path('create_review/<int:ticket_id>/',
         blog.views.create_review_from_ticket,
         name='create_review_from_ticket'),
    path('change-password', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('blog/<int:review_id>/editReview', blog.views.edit_review, name='edit_review'),
    path('blog/<int:ticket_id>/editTicket', blog.views.edit_ticket, name='edit_ticket'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
