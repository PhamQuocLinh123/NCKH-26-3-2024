import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector
import os
import pandas as pd


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Tạo thanh cuộn dọc
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(side="right", fill="y", expand=False)
        # Tạo thanh cuộn ngang
        hscrollbar = tk.Scrollbar(self, orient="horizontal")
        hscrollbar.pack(side="bottom", fill="x", expand=False)

        # Tạo canvas để chứa khung cuộn
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,
                           xscrollcommand=hscrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # Tạo khung để chứa nội dung
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("DỮ LIỆU ĐẾM TỪ ẢNH")

        # Thiết lập kích thước tối đa cho cửa sổ
        self.geometry('1400x900')
        # Tiêu đề của ứng dụng
        self.title_label = tk.Label(self, text="Đếm số lượng người từ ảnh", font=("Helvetica", 20), bg="#3366CC",
                                    fg="white")
        self.title_label.pack(pady=20)

        # Thiết lập màu nền cho cửa sổ
        self.configure(background="#3366CC")

        # Tạo khung chứa dữ liệu có thể cuộn
        self.scroll_frame = ScrollableFrame(self, bg="white")
        self.scroll_frame.pack(fill="both", expand=True)

        self.display_images()

        # Tạo nút chuyển trang
        self.create_buttons()

    def display_images(self):
        # Kết nối đến cơ sở dữ liệu MySQL
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='face_recognizer'
        )
        self.cursor = self.conn.cursor()

        # Truy vấn dữ liệu từ bảng face_count
        self.cursor.execute("SELECT id, image_name, timestamp, count FROM face_count")
        results = self.cursor.fetchall()

        row_num = 0  # Số dòng hiện tại
        col_num = 0  # Số cột hiện tại
        max_cols = 4  # Số cột tối đa trên mỗi dòng

        # Hiển thị hình ảnh, timestamp và count từ các bản ghi trong kết quả truy vấn
        for result in results:
            id = result[0]
            image_path = result[1]
            timestamp = result[2]
            count = result[3]

            image = Image.open(image_path)
            image = image.resize((350, 250), Image.BILINEAR)

            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.scroll_frame.scrollable_frame, image=photo,
                             text=f"Timestamp: {timestamp}\nCount: {count}", compound=tk.BOTTOM, bg="white")
            label.image = photo

            # Đặt khung vào dòng và cột tương ứng
            label.grid(row=row_num, column=col_num, padx=10, pady=10)

            # Thiết lập màu cho từng ô chứa dữ liệu
            if row_num % 2 == 0:
                label.configure(bg="#FF0000")
            else:
                label.configure(bg="#FF0000")

            # Khi nhấp vào một ô, gọi hàm xóa ô đó
            label.bind("<Button-1>", lambda event, widget=label, id=id: self.remove_cell(widget, id))

            col_num += 1
            if col_num == max_cols:
                row_num += 1
                col_num = 0

    def create_buttons(self):
        # Tạo style cho các nút
        style = ttk.Style()

        # Thiết lập kiểu cho nút "Đếm số người"
        style.configure("CountButton.TButton", foreground="black", background="#FFA500", font=("Helvetica", 12),
                        borderwidth=0, relief="solid", padx=10, pady=5)

        # Thiết lập kiểu cho nút "Xuất Excel"
        style.configure("ExportButton.TButton", foreground="black", background="#FFA500", font=("Helvetica", 12),
                        borderwidth=0, relief="solid", padx=10, pady=5)

        # Tạo nút "Đếm số người"
        button_count = ttk.Button(self, text="Đếm số người", command=self.open_face_count, style="CountButton.TButton")
        button_count.pack(side="left", padx=10)

        # Tạo nút "Xuất Excel"
        button_export = ttk.Button(self, text="Xuất Excel", command=self.export_to_excel, style="ExportButton.TButton")
        button_export.pack(side="left", padx=10)

    def open_face_count(self):
        # Mở trang face_count.py
        os.system("python face_count.py")

    def remove_cell(self, widget, id):
        # Hiển thị hộp thoại xác nhận trước khi xóa ô
        if messagebox.askokcancel("Xác nhận", "Bạn có chắc chắn muốn xóa ô này?"):
            # Xóa dữ liệu từ MySQL
            self.cursor.execute("DELETE FROM face_count WHERE id = %s", (id,))
            self.conn.commit()

            # Xóa ô khỏi giao diện
            widget.destroy()

    def export_to_excel(self):
        try:
            # Yêu cầu người dùng chọn nơi lưu tệp Excel
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

            # Kiểm tra xem người dùng đã chọn vị trí lưu tệp hay chưa
            if file_path:
                # Truy vấn dữ liệu từ cơ sở dữ liệu
                self.cursor.execute("SELECT id, image_name, timestamp, count FROM face_count")
                rows = self.cursor.fetchall()

                # Tạo DataFrame từ dữ liệu
                df = pd.DataFrame(rows, columns=["ID", "Image Name", "Timestamp", "Count"])

                # Xuất DataFrame ra tệp Excel
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Xuất Excel Thành công", "Dữ liệu đã được xuất ra tệp Excel thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi Xuất Excel", f"Đã xảy ra lỗi: {str(e)}")


# Khởi tạo ứng dụng
app = App()
app.mainloop()
