import tensorflow as tf
from tensorflow.keras.preprocessing.image import image_dataset_from_directory
from src.config import TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE

def load_datasets():
    train_ds = image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )
    val_ds = image_dataset_from_directory(
        VAL_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )
    return train_ds, val_ds
