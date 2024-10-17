from django.urls import path
from .views import upload_nature
from .views import upload_success

urlpatterns = [
    path('upload/nature/', upload_nature, name='upload_nature'),
    path('success/<int:file_id>/', upload_success, name='upload_success'),
]