from django.contrib import admin
from .models import LogEntry

# -----------------------------
# LogEntry model admin
# -----------------------------
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # Columns displayed in the list view
    list_display = ('timestamp', 'user', 'action', 'inventory_item', 'note')
    # Fields that can be searched using the search box
    search_fields = ('user__username', 'action', 'note', 'inventory_item__item')
    # Filters available in the right sidebar
    list_filter = ('action', 'timestamp')
