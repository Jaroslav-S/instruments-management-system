from django.urls import path
from .views import test_logging_view

urlpatterns = [
    path('test-logging/', test_logging_view, name='test-logging'),
]