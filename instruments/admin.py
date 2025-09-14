from django.contrib import admin
from .models import Inventory, Purchases, Servicing, Rentals, Disposals, Rental

# -----------------------------
# Inventory model admin
# -----------------------------
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inv_num', 'item', 'description', 'group', 'subgroup', 'subsubgroup', 'serial_number')
    search_fields = ('inv_num', 'item', 'description', 'serial_number')
    list_filter = ('group', 'subgroup', 'subsubgroup')


# -----------------------------
# Purchases model admin
# -----------------------------
@admin.register(Purchases)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'supplier', 'purchase_date', 'amount', 'currency', 'invoice')
    search_fields = ('inventory_item__item', 'supplier', 'invoice')
    list_filter = ('purchase_date', 'currency')


# -----------------------------
# Servicing model admin
# -----------------------------
@admin.register(Servicing)
class ServicingAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'supplier', 'service_date', 'amount', 'currency', 'invoice')
    search_fields = ('inventory_item__item', 'supplier', 'invoice')
    list_filter = ('service_date', 'currency')


# -----------------------------
# Rentals model admin (starý)
# -----------------------------
@admin.register(Rentals)
class RentalsAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'renter_name', 'rental_date', 'return_date', 'rental_type')
    search_fields = ('inventory_item__item', 'renter_name')
    list_filter = ('rental_type', 'rental_date')


# -----------------------------
# Rental model admin (nový, pro formulář)
# -----------------------------
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('instrument', 'user', 'start_date', 'end_date')
    search_fields = ('instrument__item', 'user__username')
    list_filter = ('start_date', 'end_date')


# -----------------------------
# Disposals model admin
# -----------------------------
@admin.register(Disposals)
class DisposalsAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'disposal_date', 'disposal_reason', 'notes')
    search_fields = ('inventory_item__item',)
    list_filter = ('disposal_reason', 'disposal_date')