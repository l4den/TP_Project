from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Account
from .forms import RegistrationForm, LoginForm
from appointments.models import Appointment


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            user = Account.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Account created')

            return redirect('login_page')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully logged in')

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home_page')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login_page')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_page(request):
    auth.logout(request)
    messages.success(request, 'Logged out')
    return redirect('login_page')
