from django.urls import path, include
from rest_framework import routers
from instruments.api.views import InventoryViewSet, PurchasesViewSet, ServicingViewSet, RentalsViewSet, DisposalsViewSet
from . import views

# REST API router
router = routers.DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'purchases', PurchasesViewSet)
router.register(r'servicing', ServicingViewSet)
router.register(r'rentals', RentalsViewSet)
router.register(r'disposals', DisposalsViewSet)

# URL patterns pro HTML views + REST API
urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),

    # HTML views (formuláře)
    path("create_rental/", views.create_rental, name="create_rental"),
    path("rental_success/", views.rental_success, name="rental_success"),
]