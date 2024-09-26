import tensorflow as tf
import matplotlib.pyplot as plt
import json

# Set paths for your local dataset
train_dir = 'backend/datasets/Fruit_imageDatasetTrain'  # e.g., 'backend/datasets/Fruit_imageDataset/train'
val_dir = 'backend/datasets/Fruit_imageDatasetVal'  # e.g., 'backend/datasets/Fruit_imageDataset/validation'
test_dir = 'backend/datasets/Fruit_imageDatasetTest'       # e.g., 'backend/datasets/Fruit_imageDataset/test'

# Step 1: Data Preparation
batch_size = 32
img_size = (64, 64)

# Load training set
training_set = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    labels="inferred",
    label_mode="categorical",  # Since we have 6 fruit classes
    batch_size=batch_size,
    image_size=img_size,
    shuffle=True,
    seed=42
)

# Load validation set
validation_set = tf.keras.utils.image_dataset_from_directory(
    val_dir,
    labels="inferred",
    label_mode="categorical",
    batch_size=batch_size,
    image_size=img_size,
    shuffle=True,
    seed=42
)

# Step 2: Build CNN Model
cnn = tf.keras.models.Sequential()

# First Convolutional Layer
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=[64, 64, 3]))
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# Add Dropout to prevent overfitting
cnn.add(tf.keras.layers.Dropout(0.25))

# Second Convolutional Layer
cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# Add Dropout again
cnn.add(tf.keras.layers.Dropout(0.25))

# Flatten before passing to dense layers
cnn.add(tf.keras.layers.Flatten())

# Dense Layers for classification
cnn.add(tf.keras.layers.Dense(units=512, activation='relu'))
cnn.add(tf.keras.layers.Dense(units=256, activation='relu'))
cnn.add(tf.keras.layers.Dropout(0.5))  # Dropout for regularization

# Output Layer for 6 classes
cnn.add(tf.keras.layers.Dense(units=6, activation='softmax'))

# Step 3: Compile the model
cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

cnn.summary()

# Step 4: Train the Model
training_history = cnn.fit(
    x=training_set,
    validation_data=validation_set,
    epochs=10  # You can increase the number of epochs based on results
)

# Step 5: Evaluate Training and Validation Accuracy
train_loss, train_acc = cnn.evaluate(training_set)
print('Training accuracy:', train_acc)

val_loss, val_acc = cnn.evaluate(validation_set)
print('Validation accuracy:', val_acc)

# Step 6: Save the Model
cnn.save('trained_fruit_model.h5')

# Save Training History
with open('training_hist.json', 'w') as f:
    json.dump(training_history.history, f)

print("Validation set Accuracy: {} %".format(training_history.history['val_accuracy'][-1] * 100))

# Step 7: Plot Accuracy and Loss
epochs_range = range(1, len(training_history.history['accuracy']) + 1)

# Plot Training Accuracy
plt.plot(epochs_range, training_history.history['accuracy'], color='red')
plt.xlabel('No. of Epochs')
plt.ylabel('Training Accuracy')
plt.title('Training Accuracy')
plt.show()

# Plot Validation Accuracy
plt.plot(epochs_range, training_history.history['val_accuracy'], color='blue')
plt.xlabel('No. of Epochs')
plt.ylabel('Validation Accuracy')
plt.title('Validation Accuracy')
plt.show()

# Step 8: Load and Evaluate Test Set (if available)
test_set = tf.keras.utils.image_dataset_from_directory(
    test_dir,  # Path to test dataset
    labels="inferred",
    label_mode="categorical",
    batch_size=batch_size,
    image_size=img_size,
    shuffle=True
)

test_loss, test_acc = cnn.evaluate(test_set)
print('Test accuracy:', test_acc)
