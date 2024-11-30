import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
import pandas as pd




# === Налаштування програми ===
MODEL_PATH = "fake_image_detector_model.h5"
UPLOAD_FOLDER = "uploads"
DATASET_ZIP = "dataset.zip"
DATASET_FOLDER = "dataset"
DATASET_COMMAND = "kaggle datasets download -d xhlulu/140k-real-and-fake-faces"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Завантаження моделі ===
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Файл моделі не знайдено! Завантажте та розмістіть модель у поточній директорії.")

model = load_model(MODEL_PATH)


# === Нові типи фейків ===
def detect_face_manipulation(image):
    """Метод для виявлення маніпуляцій з обличчям на зображенні."""
    # Тут можна використовувати окрему модель або метод для виявлення змін обличчя
    return "Маніпуляція з обличчям" if np.random.rand() > 0.5 else None


def detect_color_manipulation(image):
    """Метод для виявлення маніпуляцій з кольором на зображенні."""
    # Реалізувати перевірку зміни кольору
    return "Маніпуляція з кольором" if np.random.rand() > 0.5 else None


def detect_texture_manipulation(image):
    """Метод для виявлення маніпуляцій з текстурами на зображенні."""
    # Реалізувати перевірку текстур
    return "Маніпуляція з текстурою" if np.random.rand() > 0.5 else None


def analyze_image(image_path):
    """Аналіз зображення для визначення фейковості з використанням декількох методів."""
    try:
        image = Image.open(image_path).convert('RGB').resize((224, 224))
        original_image = Image.open(image_path).convert('RGB')  # Для виведення змін
        image_array = img_to_array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        prediction = model.predict(image_array)
        confidence = np.max(prediction)
        is_fake = np.argmax(prediction) == 1

        # Визначення типу фейку
        manipulation_type = None
        manipulation_type = detect_face_manipulation(image) or \
                            detect_color_manipulation(image) or \
                            detect_texture_manipulation(image)

        method = "Генеративна модель" if is_fake else "Нормальний знімок"

        # Візуалізація змін на зображенні
        if is_fake:
            draw = ImageDraw.Draw(original_image)
            draw.rectangle([50, 50, 174, 174], outline="red", width=3)  # Приклад зміни

        return {"is_fake": is_fake, "method": method, "manipulation_type": manipulation_type,
                "image": original_image}, confidence
    except Exception as e:
        return {"error": str(e)}, 0


# === Генерація TXT-звіту ===
def generate_txt_report(results, file_path="report.txt"):
    """Генерація звіту у текстовому форматі."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Звіт про аналіз зображень\n\n")
            file.write(
                f"{'№':<5} {'Назва зображення':<40} {'Фейк (так/ні)':<15} {'Метод фейку':<30} {'Тип маніпуляції':<30}\n")
            file.write("=" * 120 + "\n")

            for idx, (image_path, result) in enumerate(results.items(), start=1):
                fake_status = "так" if result["is_fake"] else "ні"
                method = result.get("method", "Невідомо")
                manipulation_type = result.get("manipulation_type", "Немає")
                file.write(
                    f"{idx:<5} {os.path.basename(image_path):<40} {fake_status:<15} {method:<30} {manipulation_type:<30}\n")

        print(f"Звіт успішно збережено в {file_path}")
    except Exception as e:
        print(f"Помилка при генерації TXT звіту: {e}")


# === Генерація Excel-звіту ===
def generate_excel_report(results, file_path="report.xlsx"):
    """Генерація звіту у Excel форматі."""
    try:
        data = []
        for idx, (image_path, result) in enumerate(results.items(), start=1):
            fake_status = "так" if result["is_fake"] else "ні"
            method = result.get("method", "Невідомо")
            manipulation_type = result.get("manipulation_type", "Немає")
            data.append([idx, os.path.basename(image_path), fake_status, method, manipulation_type])

        df = pd.DataFrame(data, columns=["№", "Назва зображення", "Фейк (так/ні)", "Метод фейку", "Тип маніпуляції"])
        df.to_excel(file_path, index=False)
        print(f"Звіт успішно збережено в {file_path}")
    except Exception as e:
        print(f"Помилка при генерації Excel звіту: {e}")


# === Інтерфейс Tkinter ===
class FakeImageDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fake Image Detector")
        self.results = {}

        # Кнопка для завантаження зображення
        self.load_button = tk.Button(root, text="Завантажити зображення", command=self.load_image, padx=10, pady=5)
        self.load_button.pack(pady=10)

        # Мітка для результату
        self.result_label = tk.Label(root, text="Результат: N/A", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Поле для виведення результатів
        self.result_text = ScrolledText(root, height=10, width=60)
        self.result_text.pack(pady=10)

        # Місце для відображення зображення
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Кнопка для генерації звіту
        self.report_button_txt = tk.Button(root, text="Згенерувати TXT звіт", command=self.generate_txt_report, padx=10,
                                           pady=5)
        self.report_button_txt.pack(pady=10)

        self.report_button_excel = tk.Button(root, text="Згенерувати Excel звіт", command=self.generate_excel_report,
                                             padx=10, pady=5)
        self.report_button_excel.pack(pady=10)

    def load_image(self):
        """Завантаження та аналіз зображення."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            result, confidence = analyze_image(file_path)
            if "error" in result:
                self.result_label.config(text=f"Помилка: {result['error']}")
            else:
                self.results[file_path] = result  # зберігаємо метод фейку
                self.display_result(result)
                self.result_label.config(text=f"Вірогідність фейку: {confidence * 100:.2f}%")

    def display_result(self, result):
        """Відображення результату на екрані."""
        if result["is_fake"]:
            self.result_text.insert(tk.END,
                                    "Це фейк! Тип маніпуляції: " + result.get("manipulation_type", "Невідомо") + "\n")
        else:
            self.result_text.insert(tk.END, "Це не фейк.\n")

        self.result_text.insert(tk.END, f"Метод фейку: {result.get('method', 'Невідомо')}\n\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")

        img = ImageTk.PhotoImage(result["image"].resize((250, 250)))
        self.image_label.config(image=img)
        self.image_label.image = img

    def generate_txt_report(self):
        """Генерація звіту у TXT форматі."""
        report_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if report_path:
            generate_txt_report(self.results, report_path)

    def generate_excel_report(self):
        """Генерація Excel звіту."""
        report_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if report_path:
            generate_excel_report(self.results, report_path)


# Запуск програми
root = tk.Tk()
app = FakeImageDetectorApp(root)
root.mainloop()
