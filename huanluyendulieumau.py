import dlib
import os

# Đường dẫn tới thư mục chứa dữ liệu huấn luyện
train_data_dir = "D:/Nghiên cứu khoa học-2024/face_recognizer/dataset"

# Tạo một detector khuôn mặt
detector = dlib.get_frontal_face_detector()

# Tạo một list chứa tất cả các ảnh và nhãn
images = []
labels = []

# Lặp qua từng tệp trong thư mục dữ liệu huấn luyện
for root, dirs, files in os.walk(train_data_dir):
    for file in files:
        # Đường dẫn đến ảnh
        image_path = os.path.join(root, file)

        # Đọc ảnh
        img = dlib.load_rgb_image(image_path)

        # Phát hiện khuôn mặt trong ảnh
        faces = detector(img)

        # Lấy tên người từ tên thư mục chứa ảnh
        label = os.path.basename(root)

        # Nếu có khuôn mặt được phát hiện, thêm ảnh và nhãn vào list
        if len(faces) > 0:
            images.append(img)
            labels.append(label)

# Kiểm tra xem có đủ dữ liệu để huấn luyện không
if len(images) == 0:
    print("Không tìm thấy dữ liệu huấn luyện.")
    exit()

# Khởi tạo bộ nhận diện khuôn mặt HOG (Histogram of Oriented Gradients)
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Huấn luyện mô hình nhận diện khuôn mặt
face_recognizer.train(images, labels)

# Lưu mô hình đã huấn luyện
face_recognizer.save("trained_face_recognizer.dat")

print("Huấn luyện hoàn thành và mô hình đã được lưu.")
