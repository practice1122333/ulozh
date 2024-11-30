import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, filedialog


# 1. Завантаження та підготовка даних
def load_data():
    data_gen = ImageDataGenerator(
        rescale=1. / 255,
        validation_split=0.2,
        horizontal_flip=True,
        zoom_range=0.2
    )
    train_data = data_gen.flow_from_directory(
        "dataset_path",
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    val_data = data_gen.flow_from_directory(
        "dataset_path",
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    return train_data, val_data


# 2. Побудова моделі
def build_model():
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)
    predictions = Dense(2, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    for layer in base_model.layers:
        layer.trainable = False  # Фіксуємо ваги базової моделі

    return model


# 3. Навчання моделі
def train_model(model, train_data, val_data):
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(train_data, validation_data=val_data, epochs=10)
    return model, history


# 4. Завантаження зображення для класифікації
def classify_image(model, image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return np.argmax(prediction), prediction


# 5. Інтерфейс для завантаження зображення
def upload_and_classify(model):
    Tk().withdraw()  # Сховати основне вікно Tkinter
    file_path = filedialog.askopenfilename()
    if file_path:
        label, prob = classify_image(model, file_path)
        print(f"Класифікація: {'Реальне' if label == 0 else 'Фейкове'} (Ймовірність: {prob[0][label] * 100:.2f}%)")


# Головна функція
if __name__ == "__main__":
    train_data, val_data = load_data()
    model = build_model()
    model, history = train_model(model, train_data, val_data)

    # Збереження моделі
    model.save("fake_image_detector.h5")

    # Побудова графіків
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title("Training Progress")
    plt.show()

    # Інтерфейс класифікації
    upload_and_classify(model)

