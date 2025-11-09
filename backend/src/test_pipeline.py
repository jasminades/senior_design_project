from config import TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE, EPOCHS
from data_preprocessing import create_data_generators
from model import create_cnn_model
from visualize import plot_training_history
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import os

def main():
    train_gen, val_gen = create_data_generators(
        TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE, show_examples=True
    )

    print("creating the model")
    model = create_cnn_model(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), num_classes=4)
    model.summary()

    print("training the model")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        steps_per_epoch=5,      
        validation_steps=2
    )

    print("saving the model")
    os.makedirs("checkpoints", exist_ok=True)
    model.save("checkpoints/test_model.keras")

    print("prediction")
    val_gen.reset()
    preds = model.predict(val_gen, steps=2)
    y_pred = np.argmax(preds, axis=1)
    y_true = val_gen.classes[:len(y_pred)]

 
    labels = np.unique(y_true)
    print("classification report")
    print(classification_report(
        y_true, 
        y_pred, 
        labels=labels,
        target_names=[list(val_gen.class_indices.keys())[i] for i in labels]
    ))
    print("confusion matrix")
    print(confusion_matrix(y_true, y_pred, labels=labels))

    print("visualization of the training")
    plot_training_history(history)

if __name__ == "__main__":
    main()
