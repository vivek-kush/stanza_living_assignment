from django.urls import path

from . import views

urlpatterns = [
    path('entry/', views.make_entry, name='make_entry'),
    path('info/', views.get_ledger, name='get_ledger'),
    path('final/', views.get_final_balance, name='get_ledger'),
]