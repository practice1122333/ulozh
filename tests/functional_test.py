from PIL import Image
import requests


def test_functionality(image_path):
    try:
        # Завантаження зображення
        img = Image.open(image_path)
        print(f"[INFO] Image {image_path} loaded successfully.")

        # Аналіз зображення через API
        url = "http://localhost:5000/api/analyze"  # URL вашого API
        files = {'file': open(image_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            print("[INFO] Analysis completed successfully.")
            result = response.json()
            print("Analysis Result:", result)
        else:
            print("[ERROR] API call failed:", response.status_code)

        # Генерація звіту
        with open("report.txt", "w") as report:
            report.write(f"Image: {image_path}\n")
            report.write(f"Analysis Result: {result}\n")
        print("[INFO] Report generated successfully.")
    except Exception as e:
        print("[ERROR] Functionality test failed:", e)


# Виклик тесту
test_functionality("test_image.jpg")
