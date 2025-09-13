from django.urls import path
from .views import CustomTokenObtainPairView

urlpatterns = [
    # JWT login endpoint (returns access, refresh, and user role)
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]