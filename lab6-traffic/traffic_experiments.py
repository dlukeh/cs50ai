import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


# Constants
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.2


def load_data(data_dir):
    """
    Load and preprocess all images from the GTSRB dataset.

    Expects `data_dir` to contain one subdirectory per category (0 to NUM_CATEGORIES-1),
    each holding the corresponding image files.

    Returns:
        images: NumPy array of shape (n, IMG_WIDTH, IMG_HEIGHT, 3)
                containing all resized and normalized images.
        labels: NumPy array of integer category labels aligned with `images`.
    """
    images = []
    labels = []

    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))

        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)

            img = cv2.imread(file_path)
            if img is None:
                continue

            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            img = img / 255.0

            images.append(img)
            labels.append(category)

    return np.array(images), np.array(labels)


def get_model():
    """
    Build and return a compiled convolutional neural network (CNN)
    for traffic sign classification.

    The network expects images of shape (IMG_WIDTH, IMG_HEIGHT, 3)
    and outputs a probability distribution over NUM_CATEGORIES classes.
    """
    model = tf.keras.models.Sequential()

    # Convolutional base: extract low-level features
    model.add(
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        )
    )
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Deeper convolutional layers: learn complex patterns
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(tf.keras.layers.Conv2D(128, (3, 3), activation="relu"))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Dense classifier head
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model


def main():

    # Load data
    images, labels = load_data("gtsrb")

    # One-hot encode labels
    labels = tf.keras.utils.to_categorical(labels)

    # Train/test split
    x_train, x_test, y_train, y_test = train_test_split(
        images, labels, test_size=TEST_SIZE
    )

    # Build model
    model = get_model()

    # Train model
    model.fit(x_train, y_train, epochs=10)

    # Evaluate model
    model.evaluate(x_test, y_test, verbose=2)

    # ---- Inspect misclassified images ----
    predictions = model.predict(x_test)

    misclassified = []

    for i in range(len(x_test)):
        predicted_label = np.argmax(predictions[i])
        true_label = np.argmax(y_test[i])

        if predicted_label != true_label:
            misclassified.append((x_test[i], predicted_label, true_label))

    print(f"Total misclassified images: {len(misclassified)}")

    # Show first 5 misclassified examples
    for i in range(min(5, len(misclassified))):
        img, pred, true = misclassified[i]
        plt.imshow(img)
        plt.title(f"Predicted: {pred}, True: {true}")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    main()
