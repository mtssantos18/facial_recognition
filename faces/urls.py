from django.urls import path
from . import views

urlpatterns = [
    path("faces/camera/", views.FaceDetectionAndCapture),
    # path("faces/test/", views.FaceCaptureViewTest.as_view()),
    path("faces/visualization/", views.FaceView),
    path("faces/recognition/", views.FaceDetection),
]
