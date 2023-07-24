from rest_framework.views import APIView, Request, Response, status
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import threading


# class FaceCaptureViewTest(APIView):
#     def get(self, request: Request) -> Response:
#         webcam = cv2.VideoCapture(0)

#         facial_recognition = mp.solutions.face_detection
#         draw = mp.solutions.drawing_utils
#         face_recognizer = facial_recognition.FaceDetection()

#         while webcam.isOpened():
#             validation, frame = webcam.read()

#             if not validation:
#                 break

#             image = frame
#             faces_list = face_recognizer.process(image)

#             if faces_list.detections:
#                 for face in faces_list.detections:
#                     draw.draw_detection(image, face)

#             cv2.imshow("Webcam Face", image)
#             if cv2.waitKey(5) == 27:
#                 break

#         cv2.imwrite("FacePicture.png", image)

#         webcam.release()
#         cv2.destroyAllWindows()
#         return StreamingHttpResponse(
#             frame, content_type="multipart/x-mixed-replace;boundary=frame"
#         )


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
                    if search_face:
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
    cam = FaceRecognitionAndCapture()
    return StreamingHttpResponse(
        gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
    )


@gzip.gzip_page
def FaceView(request):
    cam = VideoCamera()
    return StreamingHttpResponse(
        gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
    )


@gzip.gzip_page
def FaceDetection(request):
    cam = FaceRecognition()
    return StreamingHttpResponse(
        gen(cam), content_type="multipart/x-mixed-replace;boundary=frame"
    )
