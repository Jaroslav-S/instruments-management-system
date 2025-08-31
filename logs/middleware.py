# logs/middleware.py
import threading

from django.utils.deprecation import MiddlewareMixin

# thread-local storage for the current user
_user = threading.local()

def get_current_user():
    return getattr(_user, "value", None)

class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware that stores the current user in thread-local storage.
    It is then accessible in signals through instance._current_user.
    """

    def process_request(self, request):
        _user.value = getattr(request, "user", None)

    def process_response(self, request, response):
        _user.value = None
        return response

    def process_exception(self, request, exception):
        _user.value = None


# Helper function – sets _current_user when saving models
from django.db.models.signals import pre_save
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals

def attach_current_user(sender, instance, **kwargs):
    instance._current_user = get_current_user()

# Connect the signal for all our models
for model in [Inventory, Purchases, Servicing, Rentals, Disposals]:
    pre_save.connect(attach_current_user, sender=model)