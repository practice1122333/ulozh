import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Завантаження попередньо натренованої моделі
model = load_model("fake_image_detector_model.h5")

# Замороження базових шарів
for layer in model.layers:
    layer.trainable = False

# Додавання нових шарів
x = model.output
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)
predictions = layers.Dense(2, activation='softmax')(x)

# Створення оновленої моделі
model = Model(inputs=model.input, outputs=predictions)

# Компіляція моделі
model.compile(optimizer=Adam(learning_rate=1e-4),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Підготовка нових даних
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    'datasets',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Тренування моделі
history = model.fit(train_generator, epochs=10, steps_per_epoch=len(train_generator))

# Збереження оновленої моделі
model.save("updated_fake_image_detector_model.h5")

# Візуалізація результатів навчання
plt.plot(history.history['accuracy'], label='Accuracy')
plt.plot(history.history['loss'], label='Loss')
plt.title('Training Accuracy and Loss')
plt.xlabel('Epochs')
plt.ylabel('Value')
plt.legend()
plt.show()

# Перевірка на тестових даних
test_datagen = ImageDataGenerator(rescale=1.0 / 255)

test_generator = test_datagen.flow_from_directory(
    'path_to_test_data',  # Вкажіть шлях до ваших тестових даних
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Оцінка моделі
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test Accuracy: {test_accuracy:.2%}")
print(f"Test Loss: {test_loss:.4f}")
