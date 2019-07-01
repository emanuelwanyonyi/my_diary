# URLs for adding new entries

from django.urls import path
from entries import views

urlpatterns = [
    path('/', views.home_page, name='home'),
    path('create/', views.create_entry, name='create'),
    path('entries/', views.get_entries, name='entries'),
    path('details/<int:id>/', views.entry_details, name='details'),
    path('update/<int:id>/', views.update_entry, name='update'),
    path('delete/<int:id>/', views.delete_entry, name='delete'),
]
