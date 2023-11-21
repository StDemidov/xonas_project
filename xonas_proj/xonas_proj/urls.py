from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('admin/', admin.site.urls),
    path('comps/', include('comps.urls', namespace='comps')),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
