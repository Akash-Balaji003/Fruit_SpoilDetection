import os
import re
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm, preprocessing, model_selection, metrics, base
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "1"
import tensorflow as tf
import cv2

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set the path to the training dataset
path = 'backend/datasets/Train_File'

images, labels = [], []  # Initialize lists for images and labels

# Load training images and labels
for file in sorted(os.listdir(path)):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        # Read, resize, and convert image color from BGR to RGB
        img = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(path, file)), (128, 128)), cv2.COLOR_BGR2RGB)
        images.append(img)
        # Normalize fruit name for consistent labeling
        if "Hog Pulm" in file:
            file = file.replace("Hog Pulm", "HogPlum")
        elif "HogPulm" in file:
            file = file.replace("HogPulm", "HogPlum")
        elif "Lichi" in file:
            file = file.replace("Lichi", "Litchi")
        labels.append(re.findall("[a-zA-Z]+", file)[0])  # Extract label from filename

# Set the path to the test dataset
path = 'backend/datasets/Test_File'

# Load test images and labels
for file in sorted(os.listdir(path)):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        img = cv2.cvtColor(cv2.resize(cv2.imread(os.path.join(path, file)), (128, 128)), cv2.COLOR_BGR2RGB)
        images.append(img)
        labels.append(re.findall("[a-zA-Z]+", file)[0])  # Extract label from filename
        
# Convert images and labels to numpy arrays
images = np.array(images)
labels = np.array(labels)

# Display the shape of images and labels arrays
print(images.shape, labels.shape)

# Extract unique class names from labels
class_names = np.unique(labels)

# Create mappings for class indices and class names
class_map = {i: class_name for i, class_name in enumerate(class_names)}
reverse_class_map = {val: key for key, val in class_map.items()}

# Print the mapping of class indices to class names
print(class_map)

# Copy images to X and convert labels to their corresponding indices
X = images.copy()
y = np.array([reverse_class_map[label] for label in labels.copy()])

def visualize():
    """Visualize a subset of images and their corresponding labels."""
    plt.figure(figsize=(12, 12))
    for i in range(9):
        img, label = X[i], y[i]
        plt.subplot(3, 3, i + 1)
        plt.title(class_map[label])
        plt.imshow(img)
        plt.axis("off")
    plt.tight_layout()
    plt.show()

visualize()  # Call the visualize function to display images

# Image preprocessing (Normalization)
print(X.min(), X.max())  # Display min and max pixel values before normalization

# Normalize pixel values to range [0, 1]
X = X / 255.0
print(X.min(), X.max())  # Display min and max pixel values after normalization

# Data augmentation pipeline for image enhancement
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),  # Randomly flip images
    tf.keras.layers.RandomTranslation(0.1, 0.1)  # Randomly translate images
])

# Count the number of samples for each label
label_counts = pd.Series(y).value_counts()
label_counts

max_total = 500  # Set a maximum total for each class
X_new, y_new = [], []  # Initialize lists for augmented images and labels
X_cls_array = [X[y == i] for i in class_map.keys()]  # Group images by class

# Augment images for each class until the desired max_total is reached
for label, X_set in zip(class_map.keys(), X_cls_array):
    count = 0
    while count < max_total - label_counts[label]:  # Keep augmenting until we reach max_total
        for img in X_set:
            augmented_img = data_augmentation(np.expand_dims(img, axis=0))  # Apply data augmentation
            X_new.append(augmented_img[0])  # Append the augmented image
            y_new.append(label)  # Append the corresponding label
            count += 1
            if count >= max_total - label_counts[label]:  # Break if max total is reached
                break

X_new, y_new = np.array(X_new), np.array(y_new)  # Convert augmented lists to numpy arrays
print(X_new.shape, y_new.shape)  # Print the shape of augmented data

# Combine original and augmented data
X = np.concatenate([X, X_new])
y = np.concatenate([y, y_new])

print(X.shape, y.shape)  # Print the new shape of data

print(pd.Series(y).value_counts())  # Display the counts of each class after augmentation

# Splitting the data into training, testing, and validation sets
X_train_val, X_test, y_train_val, y_test = model_selection.train_test_split(X, y, test_size=0.1, stratify=y)  # Split off the test set
X_train, X_val, y_train, y_val = model_selection.train_test_split(X_train_val, y_train_val, test_size=0.1, stratify=y_train_val)  # Split training data into train and validation sets

print(X_train.shape, X_val.shape, X_test.shape)  # Print shapes of train, validation, and test sets

def test_uniformity(y_train, y_test, class_names):
    """Visualize the distribution of classes in training and testing sets."""
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 2, 1)
    plt.title("Training Set")
    plt.xticks(ticks=np.arange(len(class_names)))  # Set ticks for classes
    sns.histplot(y_train, bins=len(class_names))  # Plot histogram of training labels

    plt.subplot(1, 2, 2)
    plt.title("Testing Set")
    plt.xticks(ticks=np.arange(len(class_names)))  # Set ticks for classes
    sns.histplot(y_test, bins=len(class_names))  # Plot histogram of testing labels

    plt.tight_layout()
    plt.show()

test_uniformity(y_train, y_test, class_names)  # Call function to visualize class distributions

# Define the CNN model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=X_train.shape[1:]),  # Input layer
    tf.keras.layers.Conv2D(filters=200, kernel_size=(5, 5), activation="elu"),  # Convolutional layer
    tf.keras.layers.MaxPool2D(pool_size=(5, 5)),  # Pooling layer
    tf.keras.layers.Conv2D(filters=100, kernel_size=(3, 3), activation="elu"),  # Convolutional layer
    tf.keras.layers.MaxPool2D(pool_size=(3, 3)),  # Pooling layer    
    tf.keras.layers.Conv2D(filters=50, kernel_size=(3, 3), activation="elu"),  # Convolutional layer
    tf.keras.layers.MaxPool2D(pool_size=(3, 3)),  # Pooling layer
    tf.keras.layers.Flatten(),  # Flatten layer to convert 2D to 1D
    tf.keras.layers.Dense(units=200, kernel_initializer="he_normal"),  # Dense layer
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Activation("elu"),  # Activation function
    tf.keras.layers.Dense(units=100, kernel_initializer="he_normal"),  # Dense layer
    tf.keras.layers.BatchNormalization(),  # Batch normalization layer
    tf.keras.layers.Activation("elu"),  # Activation function
    tf.keras.layers.Dense(units=len(class_names), activation="softmax")  # Output layer
])

model.summary()  # Print model summary

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
cb1 = tf.keras.callbacks.EarlyStopping(patience=25, restore_best_weights=True)  # Early stopping callback

# Train the model
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_val, y_val), callbacks=[cb1])

# Plot the training history
results_ = pd.DataFrame(history.history)
results_.plot()
plt.show()

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)

print(loss, accuracy)  # Print loss and accuracy on test set

# Make predictions on the test set
y_test_pred_probs = model.predict(X_test)

# Convert predicted probabilities to class labels
y_test_pred = np.array([np.argmax(res) for res in y_test_pred_probs])

# Generate classification report
clf_report = metrics.classification_report(y_test, y_test_pred, digits=6)
print(clf_report)

# Create confusion matrix
conf_matrix = metrics.confusion_matrix(y_test, y_test_pred)
sns.heatmap(conf_matrix, annot=True)  # Visualize the confusion matrix
plt.show()

# Save the trained model to a file
model.save('backend/models/fruit_Model_v4_1.h5')
