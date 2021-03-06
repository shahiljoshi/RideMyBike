from django.urls import path
from bikes import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('stations/', views.stations, name='stations'),
    path('station/<int:station_id>/', views.station_detail, name='station_detail'),
    path('rentals/', views.user_rentals, name='rentals'),
    path('rental/<int:rental_id>/', views.rental_detail, name='rental_detail'),
    path('recharge/', views.recharge, name='recharge'),
    path('contact/', views.contactView, name='contact'),

]