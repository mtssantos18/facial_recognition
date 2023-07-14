from rest_framework.views import APIView, Request, Response, status
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import threading


# class FaceCaptureView(APIView):
#     def get(self, request: Request, camera_index: str) -> Response:
#         return Response({"message": f"Oi get {camera_index}"}, status.HTTP_200_OK)


# class FaceRecognitionView(APIView):
#     def get(self, request: Request) -> Response:
#         return Response({"message": "Oi get3"}, status.HTTP_200_OK)


class FaceRecognitionAndCapture(object):
    def __init__(self):
        # print(camera_index)
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        flip_image = cv2.flip(image, 1)
        _, jpeg = cv2.imencode(".jpg", flip_image)
        return jpeg.tobytes()

    def update(self):
        facial_recognition = mp.solutions.face_detection
        draw = mp.solutions.drawing_utils
        face_recognizer = facial_recognition.FaceDetection()
        while True:
            (self.grabbed, self.frame) = self.video.read()
            face_list = face_recognizer.process(self.frame)

            if face_list.detections:
                for face in face_list.detections:
                    search_face = draw.draw_detection(self.frame, face)
                    if search_face == True:
                        cv2.imwrite("FacePicture.png", self.frame)
                        break


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        flip_image = cv2.flip(image, 1)
        _, jpeg = cv2.imencode(".jpg", flip_image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


class FaceRecognition(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        flip_image = cv2.flip(image, 1)
        _, jpeg = cv2.imencode(".jpg", flip_image)
        return jpeg.tobytes()

    def update(self):
        facial_recognition = mp.solutions.face_detection
        draw = mp.solutions.drawing_utils
        face_recognizer = facial_recognition.FaceDetection()
        while True:
            (self.grabbed, self.frame) = self.video.read()
            face_list = face_recognizer.process(self.frame)

            if face_list.detections:
                for face in face_list.detections:
                    draw.draw_detection(self.frame, face)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@gzip.gzip_page
def FaceDetectionAndCapture(request):
    try:
        cam = FaceRecognitionAndCapture()
        return StreamingHttpResponse(
            gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except:
        pass

@gzip.gzip_page
def FaceView(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(
            gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except:
        pass

@gzip.gzip_page
def FaceDetection(request):
    try:
        cam = FaceRecognition()
        return StreamingHttpResponse(
            gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except:
        pass

