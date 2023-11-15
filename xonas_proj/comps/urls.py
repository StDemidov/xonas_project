from django.urls import path
from . import views

app_name = 'comps'

urlpatterns = [
    path('', views.cats, name='cats'),
    path('updatedb/', views.update_db, name='update'),
]