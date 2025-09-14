from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Logs
    path('logs/', include('logs.urls')),

    # Instruments app (REST API + HTML views)
    path('instruments/', include('instruments.urls')),  # teď pod /instruments/

    # Accounts (custom JWT with role)
    path("api/accounts/", include("accounts.urls")),

    # JWT refresh (access token renewal)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Frontend static pages
    path("frontend/login/", frontend_views.login_page, name="login"),
    path("frontend/menu/", frontend_views.menu_page, name="menu"),
    path("frontend/data-entry/", frontend_views.data_entry_page, name="data_entry"),
    path("frontend/view-data/", frontend_views.view_data_page, name="view_data"),

    # Redirect to login
    path('login/', frontend_views.login_page, name='login'),
]