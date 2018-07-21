from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, "homepage.html")

def eventpage(request):
    return render(request, "eventPage.html")

def godMode(request):
    return render(request, "godMode.html")