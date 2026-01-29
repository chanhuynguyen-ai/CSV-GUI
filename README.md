# CSV-GUI

CSV-GUI

CSV-GUI là ứng dụng Desktop GUI bằng Python (Tkinter) dùng để mở, xem, chỉnh sửa và xuất dữ liệu CSV một cách trực quan, không cần dùng Excel.

Ứng dụng phù hợp cho các bài toán xử lý dữ liệu cơ bản, chỉnh sửa nhanh file CSV trong các dự án kỹ thuật, sinh viên, hoặc hệ thống nhúng xuất log dữ liệu.

<img width="1152" height="829" alt="image" src="https://github.com/user-attachments/assets/2c072b12-bc5c-4a2b-9aaf-a29ef9a4cd32" />


1. Chức năng chính
1.1 Mở & hiển thị file CSV

Chọn file CSV từ máy tính

Tự động thêm cột STT (số thứ tự)

Hiển thị dữ liệu dạng bảng (giống Excel)

Có thanh cuộn ngang & dọc

1.2 Chế độ chỉnh sửa dữ liệu

Khi bấm “Điều chỉnh”, bạn có thể:

Chức năng	Mô tả
Sửa ô	Double click vào ô để sửa
Thêm hàng	Thêm dòng dữ liệu mới
Thêm cột	Tạo cột mới với tên tùy chọn
Xóa hàng	Xóa dòng đang chọn
Xóa cột	Xóa cột đang chọn
1.3 Lưu lại CSV

Ghi đè trực tiếp lên file CSV đã mở

1.4 Xuất dữ liệu sang file khác
Định dạng	Mô tả
PDF	Xuất bảng dữ liệu sang file PDF
Excel (.xlsx)	Xuất sang file Excel
2. Giao diện

Ứng dụng gồm 3 phần chính:

Thanh chọn file CSV

Bảng hiển thị dữ liệu

Thanh công cụ dưới cùng

Điều chỉnh dữ liệu

Xuất file

Lưu CSV

3. Công nghệ sử dụng
Thư viện	Vai trò
tkinter	Xây dựng giao diện GUI
pandas	Xử lý dữ liệu CSV
reportlab	Xuất file PDF
ttk.Treeview	Hiển thị bảng dữ liệu
4. Cài đặt môi trường

Bước 1: Cài Python (>= 3.8)

Bước 2: Cài thư viện cần thiết

`pip install pandas reportlab openpyxl`

openpyxl dùng để xuất file Excel.

5. Chạy chương trình

(hoặc tên file bạn lưu code)

6. Ứng dụng phù hợp cho

Sinh viên làm đồ án xử lý dữ liệu

Dự án IoT / Embedded xuất log CSV

Công cụ chỉnh sửa CSV nhẹ, không cần Excel

Ứng dụng desktop Python GUI mẫu

