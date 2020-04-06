from django.urls import path

from .views import home_view,delete_view

urlpatterns = [
    path('', home_view,name = 'home'),
    path('delete/<delete_name>/',delete_view,name = 'delete')
]
