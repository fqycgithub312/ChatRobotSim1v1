import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class ImageViewerZoom:
    def __init__(self, root):
        self.root = root
        self.root.title("图片查看器 - 支持滚轮缩放")
        self.root.geometry("1000x700")

        self.current_image = None
        self.tk_image = None
        self.image_path = None
        self.zoom_factor = 1.0
        self.base_factor = 1.0

        # 主容器
        main_container = tk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧控制面板
        left_frame = tk.Frame(main_container, width=180, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="图片查看器", font=('Microsoft YaHei', 14, 'bold'),
                 bg='#f0f0f0').pack(pady=20)

        tk.Button(left_frame, text="📂 上传图片", font=('Microsoft YaHei', 11),
                  width=14, height=2, command=self.upload_image).pack(pady=8)

        tk.Button(left_frame, text="🔍 放大", font=('Microsoft YaHei', 11),
                  width=14, height=2, command=self.zoom_in).pack(pady=4)

        tk.Button(left_frame, text="🔎 缩小", font=('Microsoft YaHei', 11),
                  width=14, height=2, command=self.zoom_out).pack(pady=4)

        tk.Button(left_frame, text="↺ 100% 原始", font=('Microsoft YaHei', 11),
                  width=14, height=2, command=self.zoom_reset).pack(pady=4)

        tk.Button(left_frame, text="🗑️ 清空", font=('Microsoft YaHei', 11),
                  width=14, height=2, command=self.clear_image).pack(pady=4)

        self.info_label = tk.Label(left_frame, text="", font=('Microsoft YaHei', 9),
                                   bg='#f0f0f0', wraplength=160, justify=tk.LEFT)
        self.info_label.pack(pady=20, padx=10)

        self.zoom_label = tk.Label(left_frame, text="", font=('Microsoft YaHei', 10, 'bold'),
                                   bg='#f0f0f0', fg='#0066cc')
        self.zoom_label.pack(pady=5)

        tk.Label(left_frame, text="\n提示：\n鼠标滚轮可放大/缩小\n按住左键可拖动图片",
                 font=('Microsoft YaHei', 8), bg='#f0f0f0', fg='#666666',
                 justify=tk.LEFT).pack(pady=10, padx=5, side=tk.BOTTOM)

        # 右侧图片显示区域 - 使用Canvas实现缩放和拖动
        right_frame = tk.Frame(main_container, bg='#2d2d2d')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建一个包含滚动条的图片区域
        self.canvas_frame = tk.Frame(right_frame, bg='#2d2d2d')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.x_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.y_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)

        self.canvas = tk.Canvas(self.canvas_frame, bg='#2d2d2d', highlightthickness=0,
                                xscrollcommand=self.x_scroll.set,
                                yscrollcommand=self.y_scroll.set)
        self.x_scroll.config(command=self.canvas.xview)
        self.y_scroll.config(command=self.canvas.yview)

        self.x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 初始提示
        self.placeholder_id = self.canvas.create_text(
            400, 300,
            text="请点击左侧「上传图片」按钮\n选择要查看的图片\n\n（鼠标滚轮可缩放图片）",
            font=('Microsoft YaHei', 12),
            fill='#aaaaaa',
            justify='center'
        )

        # 绑定鼠标滚轮事件
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Button-4>', lambda e: self.on_mouse_wheel(e, 1))
        self.canvas.bind('<Button-5>', lambda e: self.on_mouse_wheel(e, -1))

        # 绑定拖动事件
        self.canvas.bind('<ButtonPress-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.end_drag)

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False

        # 当前图片在canvas上的id
        self.image_id = None

        # 图片中心坐标
        self.image_center_x = 0
        self.image_center_y = 0

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("所有文件", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            self.current_image = Image.open(file_path)
            self.image_path = file_path
            self.zoom_factor = 1.0

            # 清除占位文字
            if self.placeholder_id is not None:
                self.canvas.delete(self.placeholder_id)
                self.placeholder_id = None

            # 初始显示：适配窗口大小
            canvas_width = max(self.canvas.winfo_width(), 700)
            canvas_height = max(self.canvas.winfo_height(), 550)
            original_width, original_height = self.current_image.size

            scale = min(canvas_width / original_width, canvas_height / original_height) * 0.9
            self.base_factor = scale
            self.zoom_factor = 1.0

            self.image_center_x = canvas_width // 2
            self.image_center_y = canvas_height // 2

            self.render_image()
            self.update_info(file_path, original_width, original_height)

        except Exception as e:
            messagebox.showerror("错误", f"无法打开图片:\n{str(e)}")

    def render_image(self):
        """根据当前缩放因子渲染图片"""
        if self.current_image is None:
            return

        original_width, original_height = self.current_image.size
        new_width = max(1, int(original_width * self.base_factor * self.zoom_factor))
        new_height = max(1, int(original_height * self.base_factor * self.zoom_factor))

        resized = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)

        # 清除旧图片
        if self.image_id is not None:
            self.canvas.delete(self.image_id)

        # 绘制新图片
        self.image_id = self.canvas.create_image(
            self.image_center_x, self.image_center_y,
            anchor=tk.CENTER,
            image=self.tk_image
        )

        # 更新滚动区域
        bbox = self.canvas.bbox(self.image_id)
        if bbox:
            self.canvas.config(scrollregion=(bbox[0] - 100, bbox[1] - 100,
                                             bbox[2] + 100, bbox[3] + 100))

        # 更新缩放显示
        total_zoom = self.base_factor * self.zoom_factor * 100
        self.zoom_label.config(text=f"缩放: {total_zoom:.1f}%")

    def on_mouse_wheel(self, event, delta=None):
        """鼠标滚轮缩放图片"""
        if self.current_image is None:
            return

        if delta is None:
            if event.delta > 0:
                zoom_delta = 1.1
            else:
                zoom_delta = 0.9
        else:
            if delta > 0:
                zoom_delta = 1.1
            else:
                zoom_delta = 0.9

        new_factor = self.zoom_factor * zoom_delta
        # 限制缩放范围
        if 0.05 <= new_factor <= 20:
            self.zoom_factor = new_factor
            self.render_image()

    def zoom_in(self):
        if self.current_image is None:
            return
        self.zoom_factor *= 1.2
        if self.zoom_factor > 20:
            self.zoom_factor = 20
        self.render_image()

    def zoom_out(self):
        if self.current_image is None:
            return
        self.zoom_factor *= 0.8
        if self.zoom_factor < 0.05:
            self.zoom_factor = 0.05
        self.render_image()

    def zoom_reset(self):
        if self.current_image is None:
            return
        self.zoom_factor = 1.0
        self.render_image()

    def start_drag(self, event):
        """开始拖动图片"""
        if self.current_image is None:
            return
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.is_dragging = True

    def on_drag(self, event):
        """拖动图片"""
        if not self.is_dragging or self.image_id is None:
            return

        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.canvas.move(self.image_id, dx, dy)

        # 更新图片中心
        bbox = self.canvas.bbox(self.image_id)
        if bbox:
            self.image_center_x = (bbox[0] + bbox[2]) // 2
            self.image_center_y = (bbox[1] + bbox[3]) // 2
            self.canvas.config(scrollregion=(bbox[0] - 100, bbox[1] - 100,
                                             bbox[2] + 100, bbox[3] + 100))

        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def end_drag(self, event):
        """结束拖动"""
        self.is_dragging = False

    def clear_image(self):
        if self.image_id is not None:
            self.canvas.delete(self.image_id)
            self.image_id = None

        self.current_image = None
        self.tk_image = None
        self.image_path = None
        self.zoom_factor = 1.0
        self.base_factor = 1.0
        self.info_label.config(text="")
        self.zoom_label.config(text="")

        # 重新显示占位文字
        canvas_width = max(self.canvas.winfo_width(), 700)
        canvas_height = max(self.canvas.winfo_height(), 550)
        self.placeholder_id = self.canvas.create_text(
            canvas_width // 2, canvas_height // 2,
            text="请点击左侧「上传图片」按钮\n选择要查看的图片\n\n（鼠标滚轮可缩放图片）",
            font=('Microsoft YaHei', 12),
            fill='#aaaaaa',
            justify='center'
        )

    def update_info(self, file_path, width, height):
        file_size = os.path.getsize(file_path)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size} 字节"

        info_text = f"文件名: {os.path.basename(file_path)}\n\n"
        info_text += f"尺寸: {width} x {height}\n\n"
        info_text += f"大小: {size_str}"
        self.info_label.config(text=info_text)


def main():
    root = tk.Tk()
    app = ImageViewerZoom(root)
    root.mainloop()


if __name__ == "__main__":
    main()