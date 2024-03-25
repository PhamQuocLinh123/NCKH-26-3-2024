import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import os
import dlib

class Database_str:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'face_recognizer'
        self.port = '3306'


class FaceCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Counter")
        self.root.geometry("600x600")  # Set window size to 800x800

        self.db = Database_str()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select an image:", font=("Arial", 12))
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.select_button = tk.Button(self.root, text="Select Image", command=self.select_image, font=("Arial", 10))
        self.select_button.grid(row=0, column=1, padx=10, pady=10)

        self.count_button = tk.Button(self.root, text="Count Faces", command=self.count_faces, font=("Arial", 10))
        self.count_button.grid(row=0, column=2, padx=10, pady=10)
        self.show_report_button = tk.Button(self.root, text="Show Face Count Report", command=self.open_show_face_count,
                                            font=("Arial", 10))
        self.show_report_button.grid(row=0, column=3, padx=10, pady=10)

        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="lightgray", highlightthickness=0)
        self.canvas.grid(row=1, columnspan=3, padx=10, pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if hasattr(self, 'image_path'):
            self.display_image()

    def display_image(self):
        self.image = cv2.imread(self.image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.resize(self.image, (400, 300))
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', self.image)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def count_faces(self):
        if hasattr(self, 'image_path'):
            num_faces, image_with_faces = self.count_faces_in_image(self.image_path)
            self.insert_face_count(self.image_path, num_faces)
            self.display_image_with_faces(image_with_faces, num_faces)
        else:
            messagebox.showerror("Error", "Please select an image first.")

    def count_faces_in_image(self, image_path):
        detector = dlib.get_frontal_face_detector()
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        # Draw bounding boxes around faces
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return len(faces), image

    def display_image_with_faces(self, image, num_faces):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (400, 300))
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', image)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.create_text(10, 10, anchor=tk.NW, text=f"Faces counted: {num_faces}", fill="red",
                                font=("Arial", 14, "bold"))

        # Save image with faces to 'img_face_count' directory
        save_dir = 'img_face_count'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, os.path.basename(self.image_path))
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        print(f"Image with faces saved to {save_path}")

    def insert_face_count(self, image_name, count):
        try:
            conn = mysql.connector.connect(
                host=self.db.host,
                user=self.db.user,
                password=self.db.password,
                database=self.db.database,
                port=self.db.port
            )
            cursor = conn.cursor()
            timestamp = datetime.now()

            # Save the image to the img_face_count directory
            save_dir = 'img_face_count'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(save_dir, os.path.basename(image_name))
            cv2.imwrite(save_path, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

            # Insert the record into the database
            cursor.execute("INSERT INTO face_count (image_name, timestamp, count) VALUES (%s, %s, %s)",
                           (save_path, timestamp, count))
            conn.commit()
            messagebox.showinfo("Success", "Face count inserted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error inserting face count: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def open_show_face_count(self):
        # Function to open show_face_count.py
        os.system("python show_face_count.py")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceCounterApp(root)
    root.mainloop()
