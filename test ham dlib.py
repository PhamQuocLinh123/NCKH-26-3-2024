import cv2
import dlib

class FaceRecognition:
    def __init__(self):
        self.isClicked = False
        self.className_atten_label = None
        self.notify_label = None

    def mark_attendance(self, i, r, n, d, face_cropped):
        if n is not None:
            n = str(n)
            self.notify_label['text'] = "Thông báo: Người dùng " + n + " không có trong danh sách"
        else:
            self.notify_label['text'] = "Thông báo: Không xác định được người dùng"

    def recognize_faces(self, img):
        # Khởi tạo bộ nhận diện khuôn mặt HOG
        detector = dlib.get_frontal_face_detector()

        # Phát hiện khuôn mặt trong ảnh
        faces = detector(img, 1)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Cắt và xử lý khuôn mặt
            face_cropped = img[y:y+h, x:x+w]
            # Gọi hàm đánh dấu điểm danh
            self.mark_attendance(None, None, None, None, face_cropped)

        return img

    def face_recog(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Thực hiện nhận diện khuôn mặt trên frame
            frame = self.recognize_faces(frame)

            # Hiển thị frame
            cv2.imshow('Face Recognition', frame)

            # Thoát nếu nhấn 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Giải phóng bộ nhớ và đóng tất cả cửa sổ OpenCV
        cap.release()
        cv2.destroyAllWindows()

# Khởi tạo đối tượng FaceRecognition
face_recognition = FaceRecognition()
# Thực hiện nhận dạng khuôn mặt
face_recognition.face_recog()
