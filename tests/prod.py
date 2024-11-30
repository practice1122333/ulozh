import time
from PIL import Image

def test_performance(image_path):
    start_time = time.time()
    try:
        # Завантаження зображення
        img = Image.open(image_path)
        # Моделювання аналізу зображення
        time.sleep(0.5)  # Імітація затримки обробки
        print(f"[INFO] Image {image_path} processed successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to process {image_path}: {e}")
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processing Time: {processing_time:.2f} seconds")
    return processing_time

# Тестування для різних розмірів зображень
image_sizes = ["small.jpg", "medium.jpg", "large.jpg"]
for img in image_sizes:
    test_performance(img)
