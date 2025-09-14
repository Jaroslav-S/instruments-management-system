from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RentalForm

def create_rental(request):
    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user  # přihlášený uživatel
            rental.save()
            return redirect("rental_success")
    else:
        form = RentalForm()
    return render(request, "instruments/create_rental.html", {"form": form})

def rental_success(request):
    return HttpResponse("Rental created successfully!")