from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('concessionnaires/', views.ConcessionnaireList.as_view(), name='concessionnaire-list'),
    path('concessionnaires/<int:pk>/', views.ConcessionnaireDetail.as_view(), name='concessionnaire-detail'),
    path('concessionnaires/<int:concession_id>/vehicules/', views.VehiculeList.as_view(), name='vehicule-list'),
    path('concessionnaires/<int:concession_id>/vehicules/<int:pk>/', views.VehiculeDetail.as_view(), name='vehicule-detail'),
    path('csrf/', views.get_csrf, name='get-csrf'),

    # Users and JWT token endpoints
    path('users/', views.UserCreate.as_view(), name='user-create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
]
