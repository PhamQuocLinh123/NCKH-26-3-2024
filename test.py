import cv2
import dlib
import mysql.connector


def recognize_faces(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_img)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        face_img = gray_img[y:y + h, x:x + w]

        # Nhận diện khuôn mặt và lấy ID của sinh viên nếu nhận diện thành công
        id, confidence = recognizer.predict(face_img)
        if confidence < 100:
            name = get_student_name(id)  # Lấy tên sinh viên từ cơ sở dữ liệu
            cv2.putText(img, f"Name: {name}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.putText(img, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)


def get_student_name(student_id):
    # Kết nối đến cơ sở dữ liệu và truy vấn tên sinh viên dựa trên ID
    # Đảm bảo rằng kết nối đến cơ sở dữ liệu và truy vấn được thực hiện đúng cách
    # Trả về tên của sinh viên dựa trên ID
    pass


# Khởi tạo camera
camera = cv2.VideoCapture(0)

# Tải detector và recognizer
detector = dlib.get_frontal_face_detector()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("classifier.xml")

while True:
    ret, img = camera.read()
    recognize_faces(img)
    cv2.imshow("Face Recognition", img)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
