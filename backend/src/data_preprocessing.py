import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import tensorflow as tf
import matplotlib.pyplot as plt

def create_data_generators(train_dir, val_dir=None, img_size=(128,128), batch_size=32, show_examples=False):
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_data = datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        train_dir,  
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    if show_examples:
        images, labels = next(train_data)
        plt.figure(figsize=(10, 8))
        num_images = min(9, images.shape[0])
        for i in range(num_images):
            plt.subplot(3, 3, i+1)
            plt.imshow(images[i])
            plt.title(list(train_data.class_indices.keys())[labels[i].argmax()])
            plt.axis('off')
        plt.tight_layout()
        plt.show()

    return train_data, val_data
