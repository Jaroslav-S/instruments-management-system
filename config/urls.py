
from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logs/', include('logs.urls')),
    path('api/', include('instruments.urls')),
# Frontend pages
    path("frontend/login/", frontend_views.login_page, name="login"),
    path("frontend/menu/", frontend_views.menu_page, name="menu"),
    path("frontend/data-entry/", frontend_views.data_entry_page, name="data_entry"),
    path("frontend/view-data/", frontend_views.view_data_page, name="view_data"),
    path('login/', RedirectView.as_view(url='/frontend/login/', permanent=False)),
]


