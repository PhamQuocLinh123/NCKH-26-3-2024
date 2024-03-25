import cv2
import dlib
import numpy as np
import mysql.connector
import os

# Kết nối cơ sở dữ liệu MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="face_recognizer"
)

# Hàm để thêm người dùng mới và mã hóa khuôn mặt vào cơ sở dữ liệu
def add_user_to_database(name, face_encoding):
    cursor = db_connection.cursor()

    # Thêm người dùng vào bảng users
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    user_id = cursor.lastrowid

    # Thêm mã hóa khuôn mặt vào bảng face_encodings
    cursor.execute("INSERT INTO face_encodings (user_id, face_encoding) VALUES (%s, %s)", (user_id, face_encoding))

    db_connection.commit()
    cursor.close()

# Khởi tạo detector và facial landmark predictor của Dlib
detector = dlib.get_frontal_face_detector()

# Tên thư mục để lưu trữ dataset
dataset_path = "D:/Nghiên cứu khoa học-2024/face_recognizer/dataset"

# Tạo thư mục dataset nếu chưa tồn tại
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Khởi tạo camera
video_capture = cv2.VideoCapture(0)

# Đếm số lượng ảnh đã ghi lại
num_images_captured = 0

while num_images_captured < 100:
    # Đọc hình ảnh từ camera
    ret, frame = video_capture.read()

    # Chuyển đổi hình ảnh sang ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt trong hình ảnh
    faces = detector(gray)

    # Lặp qua các khuôn mặt phát hiện được
    for face in faces:
        # Lấy tọa độ của khuôn mặt
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Lưu ảnh khuôn mặt vào thư mục dataset
        face_image = frame[y:y+h, x:x+w]
        image_filename = f"image_{num_images_captured}.jpg"
        image_path = os.path.join(dataset_path, image_filename)
        cv2.imwrite(image_path, face_image)

        # Trích xuất và mã hóa khuôn mặt
        face_encoding = np.array(face_image).tobytes()

        # Lưu thông tin người dùng và mã hóa khuôn mặt vào cơ sở dữ liệu
        add_user_to_database(f"User_{num_images_captured}", face_encoding)

        print(f"Captured image {num_images_captured + 1}")
        num_images_captured += 1

    # Hiển thị hình ảnh từ camera
    cv2.imshow('Video', frame)

    # Nhấn 'q' để thoát khỏi vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ hiển thị
video_capture.release()
cv2.destroyAllWindows()
