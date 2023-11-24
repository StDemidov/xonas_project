from django.urls import path
from . import views

app_name = 'comps'

urlpatterns = [
    path('', views.cats, name='cats'),
    path('list8/<slug:category_slug>', views.cat_list8, name='list8'),
    path('list14/<slug:category_slug>', views.cat_list14, name='list14'),
    path('list21/<slug:category_slug>', views.cat_list21, name='list21'),
    path('list30/<slug:category_slug>', views.cat_list30, name='list30'),
    path('list/like', views.like_item, name='like'),
    path('del/<int:id>', views.del_item, name='like_del'),
    path('favorites/', views.favorites, name='favorites'),
]
