from django.urls import path
from . import views

urlpatterns = [
    path('concessionnaires/', views.ConcessionnaireList.as_view(), name='concessionnaire-list'),
    path('concessionnaires/<int:pk>/', views.ConcessionnaireDetail.as_view(), name='concessionnaire-detail'),
    path('concessionnaires/<int:concession_id>/vehicules/', views.VehiculeList.as_view(), name='vehicule-list'),
    path('concessionnaires/<int:concession_id>/vehicules/<int:pk>/', views.VehiculeDetail.as_view(), name='vehicule-detail'),
    path('csrf/', views.get_csrf, name='get-csrf'),
]
