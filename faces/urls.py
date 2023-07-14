from django.urls import path
from . import views

urlpatterns = [
    path("faces/camera/", views.FaceDetectionAndCapture),
    path("faces/visualization/", views.FaceView),
    path("faces/recognition/", views.FaceDetection),
]
