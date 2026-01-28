import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        self.root.geometry("900x600")

        self.df = None
        self.edit_mode = False
        self.selected_cell = None

        # trạng thái mở nút con
        self.add_expanded = False
        self.del_expanded = False
        self.export_expanded = False

        # ------------------ CHỌN FILE --------------------
        file_frame = tk.Frame(root)
        file_frame.pack(pady=8, padx=5, fill=tk.X)

        self.file_entry = tk.Entry(file_frame)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

        tk.Button(file_frame, text="Chọn file CSV", command=self.load_file).pack(side=tk.LEFT)

        # ------------------ BẢNG -------------------------
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ------------------ NÚT DƯỚI ----------------------
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(fill=tk.X, padx=5, pady=8)

        # Nút điều chỉnh
        self.btn_edit = tk.Button(self.bottom_frame, text="Điều chỉnh", width=12, command=self.enable_edit)
        self.btn_edit.pack(side=tk.LEFT)

        # Frame chứa các nút con trong chế độ chỉnh sửa
        self.left_btn_frame = tk.Frame(self.bottom_frame)

        self.btn_add = tk.Button(self.left_btn_frame, text="Bổ sung", width=10, command=self.toggle_add_buttons)
        self.btn_delete = tk.Button(self.left_btn_frame, text="Xóa", width=10, command=self.toggle_delete_buttons)

        self.btn_add_row = tk.Button(self.left_btn_frame, text="Thêm hàng", width=10, command=self.add_row)
        self.btn_add_col = tk.Button(self.left_btn_frame, text="Thêm cột", width=10, command=self.add_column)

        self.btn_del_row = tk.Button(self.left_btn_frame, text="Xóa hàng", width=10, command=self.delete_row)
        self.btn_del_col = tk.Button(self.left_btn_frame, text="Xóa cột", width=10, command=self.delete_col)

        # -------------------- XUẤT FILE ----------------------
        self.btn_export = tk.Button(self.bottom_frame, text="Xuất file", width=12, command=self.toggle_export_buttons)
        self.btn_export.pack(side=tk.LEFT, padx=10)

        self.export_frame = tk.Frame(self.bottom_frame)
        self.btn_export_pdf = tk.Button(self.export_frame, text="PDF", width=10, command=self.open_pdf_export_window)
        self.btn_export_excel = tk.Button(self.export_frame, text="Excel", width=10, command=self.open_excel_export_window)

        # Nút lưu
        self.btn_save = tk.Button(self.bottom_frame, text="Lưu CSV", width=12, command=self.save_file)
        self.btn_save.pack(side=tk.RIGHT)

    # --------------------------------------------------
    # LOAD CSV
    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath: return

        try:
            self.df = pd.read_csv(filepath)

            if "STT" not in self.df.columns:
                self.df.insert(0, "STT", range(1, len(self.df)+1))
            else:
                self.df["STT"] = range(1, len(self.df)+1)

            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)
            self.show_table()

        except Exception as e:
            messagebox.showerror("Lỗi đọc file", str(e))

    # --------------------------------------------------
    # HIỂN THỊ BẢNG
    def show_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        frame = tk.Frame(self.table_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        vsb = tk.Scrollbar(frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        hsb = tk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')

        self.tree = ttk.Treeview(frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        if "STT" in self.df.columns:
            self.df["STT"] = range(1, len(self.df)+1)

        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"

        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for i, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row), iid=str(i))

        self.tree.bind("<Button-1>", self.select_cell)
        if self.edit_mode:
            self.tree.bind("<Double-1>", self.edit_cell)
        else:
            self.tree.bind("<Double-1>", lambda x: None)

    # --------------------------------------------------
    # CHẾ ĐỘ CHỈNH SỬA
    def enable_edit(self):
        if self.df is None:
            messagebox.showerror("Lỗi", "Chưa mở file CSV")
            return

        self.edit_mode = True
        self.btn_edit.pack_forget()

        self.left_btn_frame.pack(side=tk.LEFT, padx=10)
        self.btn_add.pack(side=tk.LEFT, padx=3)
        self.btn_delete.pack(side=tk.LEFT, padx=3)

        self.tree.bind("<Double-1>", self.edit_cell)

    # --------------------------------------------------
    # TOGGLE BỔ SUNG
    def toggle_add_buttons(self):
        if self.add_expanded:
            self.btn_add_row.pack_forget()
            self.btn_add_col.pack_forget()
        else:
            self.btn_add_row.pack(side=tk.LEFT, padx=3)
            self.btn_add_col.pack(side=tk.LEFT, padx=3)

            if self.del_expanded:
                self.toggle_delete_buttons()

            if self.export_expanded:
                self.toggle_export_buttons()

        self.add_expanded = not self.add_expanded

    # --------------------------------------------------
    # TOGGLE XÓA
    def toggle_delete_buttons(self):
        if self.del_expanded:
            self.btn_del_row.pack_forget()
            self.btn_del_col.pack_forget()
        else:
            self.btn_del_row.pack(side=tk.LEFT, padx=3)
            self.btn_del_col.pack(side=tk.LEFT, padx=3)

            if self.add_expanded:
                self.toggle_add_buttons()

            if self.export_expanded:
                self.toggle_export_buttons()

        self.del_expanded = not self.del_expanded

    # --------------------------------------------------
    # TOGGLE EXPORT
    def toggle_export_buttons(self):
        if self.export_expanded:
            self.export_frame.pack_forget()
            self.btn_export_pdf.pack_forget()
            self.btn_export_excel.pack_forget()
        else:
            self.export_frame.pack(side=tk.LEFT)
            self.btn_export_pdf.pack(side=tk.LEFT, padx=3)
            self.btn_export_excel.pack(side=tk.LEFT, padx=3)

            if self.add_expanded:
                self.toggle_add_buttons()

            if self.del_expanded:
                self.toggle_delete_buttons()

        self.export_expanded = not self.export_expanded

    # --------------------------------------------------
    # CHỌN Ô
    def select_cell(self, event):
        row = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if row and col:
            self.selected_cell = (int(row), int(col.replace("#",""))-1)

    # --------------------------------------------------
    # SỬA Ô
    def edit_cell(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell": return

        row = int(self.tree.identify_row(event.y))
        col = int(self.tree.identify_column(event.x).replace("#","")) - 1
        old_value = self.df.iat[row, col]

        win = tk.Toplevel(self.root)
        win.title("Chỉnh sửa ô")
        win.geometry("300x150")

        tk.Label(win, text="Giá trị mới:").pack(pady=5)
        entry = tk.Entry(win)
        entry.insert(0, old_value)
        entry.pack()

        def save_value():
            self.df.iat[row, col] = entry.get()
            self.show_table()
            win.destroy()

        def set_none():
            self.df.iat[row, col] = ""
            self.show_table()
            win.destroy()

        frame = tk.Frame(win)
        frame.pack(pady=10)
        tk.Button(frame, text="Lưu", width=10, command=save_value).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="None", width=10, command=set_none).pack(side=tk.LEFT, padx=5)

    # ==================================================
    # ===================== BỔ SUNG ====================
    # ==================================================

    def add_row(self):
        new_row = {col: "" for col in self.df.columns}
        self.df.loc[len(self.df)] = new_row
        self.show_table()

    def add_column(self):
        col_name = simpledialog.askstring("Tên cột", "Nhập tên cột mới:")
        if not col_name: return
        if col_name in self.df.columns:
            messagebox.showerror("Lỗi", "Tên cột đã tồn tại")
            return
        self.df[col_name] = ""
        self.show_table()

    # ==================================================
    # ======================== XÓA ======================
    # ==================================================

    def delete_row(self):
        if not self.selected_cell:
            messagebox.showwarning("Chọn ô", "Hãy click vào ô muốn xóa hàng")
            return
        row = self.selected_cell[0]
        if messagebox.askyesno("Xóa", f"Xóa hàng {row}?"):
            self.df = self.df.drop(index=row).reset_index(drop=True)
            self.show_table()

    def delete_col(self):
        if not self.selected_cell:
            messagebox.showwarning("Chọn ô", "Hãy click vào ô muốn xóa cột")
            return
        col = self.selected_cell[1]
        col_name = self.df.columns[col]
        if messagebox.askyesno("Xóa", f"Xóa cột '{col_name}'?"):
            self.df = self.df.drop(columns=[col_name])
            self.show_table()

    # ==================================================
    # ===================== XUẤT PDF ===================
    # ==================================================

    def open_pdf_export_window(self):
        self.open_export_window("pdf")

    def open_excel_export_window(self):
        self.open_export_window("excel")

    def open_export_window(self, mode):
        win = tk.Toplevel(self.root)
        win.title("Xuất file")
        win.geometry("400x200")

        tk.Label(win, text="Tên file:").pack(pady=5)
        filename_entry = tk.Entry(win, width=40)
        filename_entry.pack()

        path_var = tk.StringVar()
        tk.Label(win, text="Chọn nơi lưu:").pack(pady=5)

        def choose_folder():
            folder = filedialog.askdirectory()
            if folder:
                path_var.set(folder)

        path_frame = tk.Frame(win)
        path_frame.pack()
        tk.Entry(path_frame, textvariable=path_var, width=30).pack(side=tk.LEFT)
        tk.Button(path_frame, text="Chọn", command=choose_folder).pack(side=tk.LEFT, padx=5)

        def export():
            name = filename_entry.get()
            folder = path_var.get()

            if not name or not folder:
                messagebox.showerror("Lỗi", "Hãy nhập tên file và chọn nơi lưu!")
                return

            if mode == "pdf":
                filepath = f"{folder}/{name}.pdf"
                self.export_pdf(filepath)
            else:
                filepath = f"{folder}/{name}.xlsx"
                self.df.to_excel(filepath, index=False)

            messagebox.showinfo("OK", "Xuất file thành công!")
            win.destroy()

        frame = tk.Frame(win)
        frame.pack(pady=15)

        tk.Button(frame, text="Xác nhận", width=12, command=export).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Trở về", width=12, command=win.destroy).pack(side=tk.LEFT, padx=5)

    def export_pdf(self, filepath):
        data = [list(self.df.columns)] + self.df.values.tolist()
        pdf = SimpleDocTemplate(filepath, pagesize=letter)
        table = Table(data)
        pdf.build([table])

    # ==================================================
    # ======================= LƯU CSV ====================
    # ==================================================

    def save_file(self):
        filepath = self.file_entry.get()
        try:
            self.df.to_csv(filepath, index=False)
            messagebox.showinfo("OK", "Đã lưu CSV!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


# --------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
