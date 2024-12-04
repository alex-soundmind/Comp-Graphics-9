import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import numpy as np
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Лабораторная работа №9")
        self.pack()
        self.create_widgets()
        self.original_image = None
        self.low_pass_image = None
        self.high_pass_image = None

    def create_widgets(self):
        button_width = 30 

        self.open_button = tk.Button(self, width=button_width)
        self.open_button["text"] = "Открыть изображение"
        self.open_button["command"] = self.open_image
        self.open_button.pack(side="top")

        self.low_pass_button = tk.Button(self, width=button_width)
        self.low_pass_button["text"] = "Свёрточный фильтр низких частот"
        self.low_pass_button["command"] = self.low_pass_transform
        self.low_pass_button.pack(side="top")

        self.high_pass_button = tk.Button(self, width=button_width)
        self.high_pass_button["text"] = "Свёрточный фильтр высоких частот"
        self.high_pass_button["command"] = self.high_pass_transform
        self.high_pass_button.pack(side="top")

        self.save_low_pass_button = tk.Button(self, width=button_width)
        self.save_low_pass_button["text"] = "Сохранить результат ФНЧ"
        self.save_low_pass_button["command"] = self.save_low_pass_result
        self.save_low_pass_button.pack(side="top")

        self.save_high_pass_button = tk.Button(self, width=button_width)
        self.save_high_pass_button["text"] = "Сохранить результат ФВЧ"
        self.save_high_pass_button["command"] = self.save_high_pass_result
        self.save_high_pass_button.pack(side="top")

        self.image_label_original = tk.Label(self)
        self.image_label_original.pack(side="left")

        self.image_label_low_pass = tk.Label(self)
        self.image_label_low_pass.pack(side="left")

        self.image_label_high_pass = tk.Label(self)
        self.image_label_high_pass.pack(side="left")

    def open_image(self):
        path = filedialog.askopenfilename()
        self.original_image = Image.open(path)
        self.display_image(self.original_image, self.image_label_original)
        self.low_pass_image = self.original_image.copy()
        self.high_pass_image = self.original_image.copy()

    def low_pass_transform(self):
        if self.low_pass_image:
            width, height = self.low_pass_image.size
            self.low_pass_image = self.low_pass_image.resize((width // 2, height // 2))
            self.low_pass_image = self.low_pass_image.resize(self.original_image.size, Image.NEAREST)
            self.display_image(self.low_pass_image, self.image_label_low_pass)

    def high_pass_transform(self):
        if self.high_pass_image:
            array = np.array(self.high_pass_image)
            left_half = array[:, :array.shape[1] // 2]
            right_half = array[:, array.shape[1] // 2:]

            left_half = Image.fromarray(left_half).filter(ImageFilter.FIND_EDGES)
            right_half = Image.fromarray(right_half).filter(ImageFilter.CONTOUR)

            combined = np.hstack((left_half, right_half))
            self.high_pass_image = Image.fromarray(combined)
            self.display_image(self.high_pass_image, self.image_label_high_pass)

    def save_low_pass_result(self):
        if self.low_pass_image:
            self.save_image(self.low_pass_image, "low_pass_output.jpg")

    def save_high_pass_result(self):
        if self.high_pass_image:
            self.save_image(self.high_pass_image, "high_pass_output.jpg")

    def save_image(self, image, filename):
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=filename)
        if filepath:
            image.save(filepath)

    def display_image(self, image, label):
        image_tk = ImageTk.PhotoImage(image)
        label.config(image=image_tk)
        label.image = image_tk

root = tk.Tk()
app = Application(master=root)
app.mainloop()
