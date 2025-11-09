import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import tensorflow as tf
from config import TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE, EPOCHS
from data_preprocessing import create_data_generators
from model import create_cnn_model
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from visualize import plot_training_history


train_gen, val_gen = create_data_generators(TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE)
model = create_cnn_model(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), num_classes=4)

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
checkpoint = ModelCheckpoint("../checkpoints/model_best.keras", save_best_only=True, monitor='val_accuracy')
early_stop = EarlyStopping(patience=5, restore_best_weights=True)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint, early_stop]
)

model.save("../checkpoints/model_best.keras")

val_gen.reset()
preds = model.predict(val_gen, verbose=1)
y_pred = np.argmax(preds, axis=1)
y_true = val_gen.classes

print("classification report:")
print(classification_report(y_true, y_pred, target_names=list(val_gen.class_indices.keys())))
print("confusion matrix:")
print(confusion_matrix(y_true, y_pred))
plot_training_history(history)
