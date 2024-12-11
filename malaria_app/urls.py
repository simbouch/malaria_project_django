from django.urls import path
from malaria_app import views

# URL patterns for the app, linking URLs to specific views in views.py
urlpatterns = [
    path('', views.index, name='index'),  # Root URL, linked to the index view
    path('upload/', views.upload, name='upload'),  # URL for uploading an image
    path('result/', views.result, name='result'),  # URL for displaying the prediction result
]

from django.conf import settings
from django.conf.urls.static import static

# Adding a static files handler for development mode.
# This allows serving static files (CSS, JavaScript, images) during development.
# In production, static files are typically served by a web server like Nginx or Apache.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
