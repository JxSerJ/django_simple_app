from django.urls import path
from . import views

urlpatterns = [
    path('create_initial_data/', views.create_initial_data, name='create_initial_data'),
    path('create_client/', views.create_client, name='create_client'),
    path('create_product/', views.create_product, name='create_product'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_order_detail/', views.create_order_detail, name='create_order_detail'),
    path('delete_order/', views.delete_order, name='delete_order'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('client_orders/<int:client_id>', views.client_orders, name='update_order'),
]
