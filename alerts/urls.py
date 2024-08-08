# alerts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.alert_list, name='alert_list'),
    path('map/', views.alert_map, name='alert_map'),
    path('alert_data/', views.alert_data, name='alert_data'),
    path('create/', views.create_alert, name='create_alert'),
    path('<int:alert_id>/delete/', views.delete_alert, name='delete_alert'),
    path('contacts/', views.contacts, name='contacts'),
    path('unpublish/', views.unpublish_alert, name='unpublish_alert'),
]