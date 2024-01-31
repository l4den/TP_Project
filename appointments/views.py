import json
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from shops.models import Shop
from .forms import AppointmentForm
from .models import Appointment


@login_required
def book_appointment_page(request, id):
    shop = get_object_or_404(Shop, id=id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, shop=shop, user=request.user.get_account())
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.shop = shop
            appointment.user = request.user.get_account()

            duration = timedelta()
            price_total = 0
            service_ids = list()
            service_names = list()
            for service in form.cleaned_data['services']:
                service_ids.append(service.id)
                service_names.append(service.service)
                duration += timedelta(hours=service.time_to_complete.hour,
                                      minutes=service.time_to_complete.minute)
                price_total += service.price

            start_time = form.cleaned_data['start_time']

            end_time = timedelta(hours=start_time.hour, minutes=start_time.minute) + duration
            duration = str(duration)

            # session create
            appointment_data = model_to_dict(form.instance)
            appointment_data['date'] = str(appointment_data['date'])

            appointment_data['start_time'] = form.cleaned_data['start_time'].strftime('%H:%M:%S')
            appointment_data['end_time'] = str(end_time) #.strftime('%H:%M:%S')
            appointment_data['duration'] = duration
            appointment_data['total_price'] = price_total
            appointment_data['services'] = service_ids

            request.session['appointment_form_data'] = json.dumps(appointment_data)
            request.session['names_of_services'] = ', '.join(service_names)

            return redirect('confirm_appointment_page', id=id)  # Redirect to a success page

    else:
        form = AppointmentForm(shop=shop, user=request.user.get_account())

    appointments = Appointment.objects.filter(shop=shop, date__gte=datetime.now().today()).order_by('date', 'start_time')
    context = {'form': form, 'appointments': appointments}
    return render(request, 'appointments/appointment.html', context)


@login_required
def confirm_appointment_page(request, id):
    shop = get_object_or_404(Shop, id=id)

    session_data = request.session.get('appointment_form_data')
    submitted_data = json.loads(session_data)

    if request.method == 'POST':
        appointment_form = AppointmentForm(shop=shop, data=submitted_data, user=request.user.get_account())

        if appointment_form.is_valid():
            if 'confirm' in request.POST:
                # Convert the stored time strings back to time objects
                submitted_data['start_time'] = datetime.strptime(
                    submitted_data['start_time'], '%H:%M:%S').time()
                submitted_data['end_time'] = datetime.strptime(
                    submitted_data['end_time'], '%H:%M:%S').time()
                submitted_data['duration'] = datetime.strptime(
                    submitted_data['duration'], '%H:%M:%S').time()

                appointment = appointment_form.save(commit=False)
                appointment.__dict__.update(submitted_data)
                appointment.shop = shop
                appointment.user = request.user.get_account()
                appointment.save()
                return redirect('myappointments_page')
            elif 'change' in request.POST:
                return redirect('book_appointment_page', id=id)
        else:
            print(f'Form errors:\n{appointment_form.errors}')

    servNames = request.session.get('names_of_services')
    context = {'shop': shop, 'submitted_data': submitted_data, 'names_of_services': servNames}
    return render(request, 'appointments/confirm_appointment.html', context)


@login_required()
def myappointments_page(request):
    user = request.user.get_account()
    appointments = Appointment.objects.filter(user=user, date__gte=datetime.now().today()).order_by('date', 'start_time')

    context = {'appointments': appointments, 'now': datetime.now()}

    return render(request, 'appointments/account_appointments.html', context)


@login_required()
def confirm_delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    context = {'appointment': appointment}
    return render(request, 'appointments/delete_appointment.html', context)


@login_required()
def delete_appointment(request, id):
    apppointment = get_object_or_404(Appointment, id=id)
    apppointment.delete()
    return redirect('myappointments_page')


@login_required()
def past_appointments_page(request):
    user = request.user.get_account()
    now = datetime.now()
    appointments = Appointment.objects.filter(Q(user=user, date__lt=now.date()) |
                                              Q(user=user, date=now.date(), end_time__lt=now)
                                              ).order_by('-date', 'start_time')
    context = {'appointments': appointments}
    return render(request, 'appointments/past_appointments.html', context)