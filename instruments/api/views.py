from rest_framework import viewsets
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals
from instruments.api.serializers import InventorySerializer, PurchasesSerializer, ServicingSerializer, RentalsSerializer, DisposalsSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer

class ServicingViewSet(viewsets.ModelViewSet):
    queryset = Servicing.objects.all()
    serializer_class = ServicingSerializer

class RentalsViewSet(viewsets.ModelViewSet):
    queryset = Rentals.objects.all()
    serializer_class = RentalsSerializer

class DisposalsViewSet(viewsets.ModelViewSet):
    queryset = Disposals.objects.all()
    serializer_class = DisposalsSerializer
