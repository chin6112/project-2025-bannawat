from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('history/', views.history, name="history"),
    
    # Queue URLs
    path('queue/create/', views.queue_create, name="queue_create"),
    path('queue/<int:pk>/edit/', views.queue_edit, name="queue_edit"),
    path('queue/<int:pk>/delete/', views.queue_delete, name="queue_delete"),
    
    # Car URLs
    path('cars/', views.car_list, name="car_list"),
    path('cars/create/', views.car_create, name="car_create"),
    path('cars/<int:pk>/edit/', views.car_edit, name="car_edit"),
    path('cars/<int:pk>/delete/', views.car_delete, name="car_delete"),
    
    # Driver URLs
    path('drivers/', views.driver_list, name="driver_list"),
    path('drivers/create/', views.driver_create, name="driver_create"),
    path('drivers/<int:pk>/edit/', views.driver_edit, name="driver_edit"),
    path('drivers/<int:pk>/delete/', views.driver_delete, name="driver_delete"),
    
    path('logout/', views.logout_view, name="logout"),

    path("api/queue/create/", views.api_queue_create, name="api_queue_create"),
    path("api/queue/today/", views.api_queue_today, name="api_queue_today"),
    path("api/queue/cancel/", views.api_queue_cancel, name="api_queue_cancel"),
]
