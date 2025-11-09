from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

model = load_model("../checkpoints/model_best.keras")
class_names = ["MildDemented", "ModerateDemented", "NonDemented", "VeryMildDemented"]
IMG_SIZE = (224, 224)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize(IMG_SIZE)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)

        preds = model.predict(arr)
        idx = np.argmax(preds)
        confidence = float(preds[0][idx])

        return {
            "prediction": class_names[idx],
            "confidence": f"{confidence * 100:.2f}%"
        }

    except Exception as e:
        return {"error": str(e)}
