""" URL configuration for demetrius project.
"""
from django.contrib import admin
from django.urls import path, include

from library.views import view_data


urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path(
        '',
        view_data,
        name='view-data'
    ),
]
