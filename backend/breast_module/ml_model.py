import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import InputLayer
import tensorflow as tf
import h5py
import json
import os
from tensorflow.keras import mixed_precision

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'breast_cancer_model.h5')

def fix_model_config(path):
    with h5py.File(path, 'r+') as f:
        model_config = f.attrs.get('model_config')

        if not model_config:
            return

        # decode if bytes
        if isinstance(model_config, bytes):
            model_config = model_config.decode('utf-8')

        config = json.loads(model_config)

        modified = False

        for layer in config['config']['layers']:
            if layer['class_name'] == 'InputLayer':
                layer_config = layer['config']

                if 'batch_shape' in layer_config:
                    layer_config['batch_input_shape'] = layer_config.pop('batch_shape')
                    modified = True

        # only rewrite if needed
        if modified:
            f.attrs['model_config'] = json.dumps(config).encode('utf-8')
            print("✅ Fixed model config (batch_shape → batch_input_shape)")

# Always run fix BEFORE loading
fix_model_config(MODEL_PATH)

model = load_model(
    MODEL_PATH,
    compile=False,
    custom_objects={
        "DTypePolicy": mixed_precision.Policy
    }
)

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Invalid image or path")

    img = cv2.resize(img, (64, 64))
    img = img / 255.0
    img = np.reshape(img, (1, 64, 64, 3))

    return img


def predict_image(image_path):
    if model is None:
        raise RuntimeError("Model not loaded")

    try:
        img = preprocess_image(image_path)

        prediction = model.predict(img)

        benign_prob = float(prediction[0][0])
        malignant_prob = float(prediction[0][1])

        if benign_prob > malignant_prob:
            result = "Benign"
            confidence = benign_prob
        else:
            result = "Malignant"
            confidence = malignant_prob

        return {
            "result": result,
            "confidence": round(confidence * 100, 2),
            "raw": {
                "benign": benign_prob,
                "malignant": malignant_prob
            }
        }

    except Exception as e:
        return {
            "error": str(e)
        }