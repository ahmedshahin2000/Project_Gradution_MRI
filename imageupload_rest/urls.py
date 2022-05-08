
from django.urls import path
from .viewsets import FileUploadView


urlpatterns = [
    path('upload_image', FileUploadView.as_view()),
]