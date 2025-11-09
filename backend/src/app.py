from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model_path = "../checkpoints/model_best.keras"
model = load_model(model_path)
class_names = ["MildDemented", "ModerateDemented", "NonDemented", "VeryMildDemented"]
IMG_SIZE = (224, 224)

@app.route("/")
def home():
    return jsonify({"message": "backend is running successfully"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        img = Image.open(file.stream).convert("RGB")
        img = img.resize(IMG_SIZE)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)

        preds = model.predict(arr)
        idx = np.argmax(preds)
        confidence = preds[0][idx] * 100
        result = class_names[idx]

        return jsonify({
            "prediction": result,
            "confidence": f"{confidence:.2f}%"
        })

    except Exception as e:
        print("Error in /predict:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
