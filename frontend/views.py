from django.shortcuts import render

# just static pages, login via REST API + JS
def menu_page(request):
    return render(request, "frontend/menu.html")

def data_entry_page(request):
    return render(request, "frontend/data_entry.html")

def view_data_page(request):
    return render(request, "frontend/view_data.html")