# logs/views.py
from django.http import JsonResponse
from instruments.models import Inventory
from logs.models import LogEntry
from django.contrib.auth.decorators import login_required

@login_required
def test_logging_view(request):
    user = request.user

    # 1. Create a new Inventory item
    item = Inventory(
        group='TG',
        subgroup='TSG',
        subsubgroup='TSSG',
        item='TestItem',
        description='Initial description',
    )
    item._current_user = user
    item.save()

    # 2. Update the item
    item.description = 'Updated description'
    item._current_user = user
    item.save()

    # 3. Delete the item
    item._current_user = user
    item.delete()

    # 4. Retrieve all log entries
    logs = LogEntry.objects.all().values('user__username', 'action', 'timestamp', 'inventory_item')

    return JsonResponse(list(logs), safe=False)