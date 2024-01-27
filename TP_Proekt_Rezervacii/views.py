from django.shortcuts import render


def home_page(request):
    return render(request, 'index.html')


def contact_page(request):
    return render(request, 'contact.html')