import tensorflow as tf
import os
# Перевірка, чи імпортовані всі необхідні компоненти
try:
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
    from tensorflow.keras.models import Model
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.optimizers import Adam
    print("Імпорти успішно виконано.")
except ImportError as e:
    print(f"Помилка при імпорті: {e}")


# === Налаштування ===
DATA_DIR = "dataset/train"  # Папка з тренувальними даними
VALIDATION_DIR = "dataset/validation"  # Папка з валідаційними даними
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Отримуємо директорію виконуваного файлу
MODEL_PATH = os.path.join(SCRIPT_DIR, "fake_image_detector_model.h5")  # Збереження моделі в тій самій папці
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

# === Завантаження базової моделі ===
base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
predictions = Dense(2, activation="softmax")(x)  # 2 класи: Fake і Real

# Створення моделі
model = Model(inputs=base_model.input, outputs=predictions)

# Заморожування базових шарів
for layer in base_model.layers:
    layer.trainable = False

# === Компіляція моделі ===
model.compile(optimizer=Adam(learning_rate=0.0001), loss="categorical_crossentropy", metrics=["accuracy"])

# === Генератори даних ===
train_datagen = ImageDataGenerator(rescale=1.0 / 255, horizontal_flip=True, rotation_range=20)
validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
)
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
)

# === Навчання моделі ===
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_steps=validation_generator.samples // BATCH_SIZE,
)

# === Збереження моделі ===
model.save(MODEL_PATH)
print(f"Модель збережено у {MODEL_PATH}")
