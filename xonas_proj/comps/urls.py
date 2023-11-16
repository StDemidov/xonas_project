from django.urls import path
from . import views

app_name = 'comps'

urlpatterns = [
    path('', views.cats, name='cats'),
    path('list/<slug:category_slug>', views.cat_list, name='list'),
]