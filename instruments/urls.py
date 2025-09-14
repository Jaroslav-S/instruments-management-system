from django.urls import path, include
from rest_framework import routers
from instruments.api.views import InventoryViewSet, PurchasesViewSet, ServicingViewSet, RentalsViewSet, DisposalsViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'purchases', PurchasesViewSet)
router.register(r'servicing', ServicingViewSet)
router.register(r'rentals', RentalsViewSet)
router.register(r'disposals', DisposalsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("rentals/new/", views.create_rental, name="create_rental"),
    path("rentals/success/", views.rental_success, name="rental_success"),
]