from django.shortcuts import render

def login_page(request):
    return render(request, "frontend/login.html")

def menu_page(request):
    return render(request, "frontend/menu.html")

def data_entry_page(request):
    return render(request, "frontend/data_entry.html")

def view_data_page(request):
    return render(request, "frontend/view_data.html")