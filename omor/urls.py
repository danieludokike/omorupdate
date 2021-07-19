from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('omorapp.urls')),
    path("account/", include("django.contrib.auth.urls")),
]
