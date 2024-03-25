import tkinter as tk
from tkinter import filedialog
import cv2
import mysql.connector
import PIL.Image
import PIL.ImageTk

class FaceRecognitionSystem:
    def __init__(self):
        self.isClicked = False
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'face_recognizer'
        self.port = '3306'

        self.root = tk.Tk()
        self.root.title("Face Recognition")

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.select_button = tk.Button(self.left_frame, text="Chọn ảnh", command=self.select_image)
        self.select_button.pack(pady=10)

        self.image_label = tk.Label(self.left_frame)
        self.image_label.pack(pady=10)

        self.result_label = tk.Label(self.right_frame)
        self.result_label.pack(pady=10)

    def mark_attendance(self, student_id, roll, name, class_name, face_image):
        # Thực hiện thao tác ghi điểm danh vào cơ sở dữ liệu hoặc hệ thống quản lý sinh viên
        # Viết code để ghi thông tin vào cơ sở dữ liệu hoặc hệ thống quản lý sinh viên ở đây
        pass

    def select_image(self):
        image_path = filedialog.askopenfilename()  # Hiển thị hộp thoại chọn tệp và lưu đường dẫn tệp hình ảnh được chọn
        if image_path:
            self.recognize_face(image_path)

    def recognize_face(self, image_path):
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        img = cv2.imread(image_path)

        if img is None:
            print("Không thể đọc được ảnh từ đường dẫn.")
            return

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

        conn = mysql.connector.connect(host=self.host, user=self.user,
                                       password=self.password, database=self.database,
                                       port=self.port)
        my_cursor = conn.cursor()

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 25, 255), 2)
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))

            my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
            student_info = my_cursor.fetchone()

            if confidence >82:
                if student_info:
                    name, = student_info
                    cv2.putText(img, f"Name: {name}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    self.mark_attendance(id, None, name, None, gray_image[y:y + h, x:x + w])
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (800, 800))  # Điều chỉnh kích thước ảnh
        img = PIL.Image.fromarray(img)
        img = PIL.ImageTk.PhotoImage(img)
        self.result_label['image'] = img
        self.result_label.image = img

        conn.close()

    def start_recognition(self):
        self.root.mainloop()

# Khởi tạo hệ thống nhận dạng khuôn mặt và bắt đầu nhận
face_recognition_system = FaceRecognitionSystem()
face_recognition_system.start_recognition()
