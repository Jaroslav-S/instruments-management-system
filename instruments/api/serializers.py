from rest_framework import serializers
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'

class ServicingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicing
        fields = '__all__'

class RentalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rentals
        fields = '__all__'

class DisposalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disposals
        fields = '__all__'