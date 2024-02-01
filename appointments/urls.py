from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/book/', views.book_appointment_page, name='book_appointment_page'),
    path('confirm/<int:id>', views.confirm_appointment_page, name='confirm_appointment_page'),
    path('myappointments', views.myappointments_page, name='myappointments_page'),
    path('delete/<int:id>', views.delete_appointment, name='delete_appointment'),
    path('confirm-delete/<int:id>', views.confirm_delete_appointment, name='confirm_delete_appointment_page'),
    path('past-appointments', views.past_appointments_page, name='past_appointments_page'),
]

