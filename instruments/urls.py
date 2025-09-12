from django.urls import path, include
from rest_framework import routers
from .api import InventoryViewSet, PurchasesViewSet, ServicingViewSet, RentalsViewSet, DisposalsViewSet

router = routers.DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'purchases', PurchasesViewSet)
router.register(r'servicing', ServicingViewSet)
router.register(r'rentals', RentalsViewSet)
router.register(r'disposals', DisposalsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]