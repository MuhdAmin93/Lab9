import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Лабораторная работа №9")
        self.pack(padx=10, pady=10)
        self.create_widgets()
        self.original_image = None
        self.low_pass_image = None
        self.high_pass_image = None

    def create_widgets(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", fill="x", pady=5)
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(side="bottom", fill="both", expand=True, pady=10)

        button_width = 20

        self.open_button = tk.Button(self.button_frame, width=button_width, text="Открыть изображение", command=self.open_image)
        self.open_button.pack(side="left", padx=5)

        self.image_label_original = tk.Label(self.image_frame, text="Оригинал")
        self.image_label_original.grid(row=0, column=0, padx=10, pady=10)

        self.image_label_low_pass = tk.Label(self.image_frame, text="Результат ФНЧ")
        self.image_label_low_pass.grid(row=0, column=1, padx=10, pady=10)

        self.image_label_high_pass = tk.Label(self.image_frame, text="Результат ФВЧ")
        self.image_label_high_pass.grid(row=0, column=2, padx=10, pady=10)

    def open_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = Image.open(path)
            self.display_image(self.original_image, self.image_label_original)
            self.low_pass_transform()
            self.high_pass_transform()

    def low_pass_transform(self):
        if self.original_image:
            width, height = self.original_image.size
            left_half = self.original_image.crop((0, 0, width // 2, height))
            right_half = self.original_image.crop((width // 2, 0, width, height))

            # ФНЧ для левой половины на красном канале
            left_np = np.array(left_half)
            left_np[:, :, 0] = Image.fromarray(left_np[:, :, 0]).filter(ImageFilter.GaussianBlur(10))
            left_result = Image.fromarray(left_np)

            # ФНЧ для правой половины на зелёном канале
            right_np = np.array(right_half)
            right_np[:, :, 1] = Image.fromarray(right_np[:, :, 1]).filter(ImageFilter.GaussianBlur(10))
            right_result = Image.fromarray(right_np)

            # Собираем результат
            result = Image.new("RGB", (width, height))
            result.paste(left_result, (0, 0))
            result.paste(right_result, (width // 2, 0))

            self.low_pass_image = result
            self.display_image(self.low_pass_image, self.image_label_low_pass)

    def high_pass_transform(self):
        if self.original_image:
            width, height = self.original_image.size

            # ШАГ 1: Применяем фильтр серого только к правой половине
            right_half = self.original_image.crop((width // 2, 0, width, height)).convert("L")

            # Объединяем обе половины в одно изображение
            half_gray_image = Image.new("RGB", (width, height))
            half_gray_image.paste(self.original_image.filter(ImageFilter.FIND_EDGES).crop((0, 0, width // 2, height)), (0, 0))  # Левая половина цветная
            half_gray_image.paste(right_half.convert("RGB"), (width // 2, 0))  # Правая половина серого цвета


            # ШАГ 2: Применяем лапласиан гауссиана ко всему изображению
            laplacian_image = half_gray_image.filter(ImageFilter.FIND_EDGES)

            # Обновляем изображение и отображаем результат
            self.high_pass_image = half_gray_image
            self.display_image(self.high_pass_image, self.image_label_high_pass)


    def display_image(self, image, label):
        image_tk = ImageTk.PhotoImage(image)
        label.config(image=image_tk)
        label.image = image_tk

root = tk.Tk()
app = Application(master=root)
app.mainloop()
