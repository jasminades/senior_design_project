import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR = os.path.join(BASE_DIR, "data", "train")
VAL_DIR = os.path.join(BASE_DIR, "data", "val")
IMG_SIZE = (224, 224)
BATCH_SIZE = 8
NUM_CLASSES = 4
EPOCHS = 2
LEARNING_RATE = 0.001

