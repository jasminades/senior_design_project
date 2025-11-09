import os
import matplotlib.pyplot as plt
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import tensorflow as tf
from tensorflow.keras.models import load_model
from data_preprocessing import create_data_generators
from config import TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

def main():
    _, val_gen = create_data_generators(TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE, show_examples=False)
    model = load_model("../checkpoints/model_best.keras")

    val_gen.reset()
    preds = model.predict(val_gen, verbose=1)
    y_pred = np.argmax(preds, axis=1)
    y_true = val_gen.classes[:len(y_pred)] 

    class_names = list(val_gen.class_indices.keys())
    print("\nClassification report")
    print(classification_report(y_true, y_pred, target_names=class_names))

    print("\nConfusion matrix")
    print(confusion_matrix(y_true, y_pred))

if __name__ == "__main__":
    main()