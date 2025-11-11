from django.shortcuts import render


def consultations(request):
    return render(request, "consultations.html")
