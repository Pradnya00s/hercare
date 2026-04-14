"""
Ultrasound Image CNN Prediction Module
======================================
Handles loading the pre-trained CNN model (model.h5) and processing 
ultrasound images for PCOS prediction.

Author: HerCare Team
"""

import os
import numpy as np
from tensorflow import keras
from PIL import Image
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Model path configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# allow either an HDF5 file (model.h5) or a SavedModel folder
MODEL_FOLDER = os.path.join(BASE_DIR, "pcos_screener/model")
# default file-based paths (check both common names)
DEFAULT_H5 = os.path.join(MODEL_FOLDER, "model.h5")
ALTERNATE_H5 = os.path.join(MODEL_FOLDER, "pcosmodel.h5")
# directory-based SavedModel
SAVED_MODEL_DIR = os.path.join(MODEL_FOLDER, "pcos_ultrasound_model")

# decide which path to use at runtime
# if either of the H5 files exist, use them in priority order
if os.path.exists(DEFAULT_H5):
    CNN_MODEL_PATH = DEFAULT_H5
elif os.path.exists(ALTERNATE_H5):
    CNN_MODEL_PATH = ALTERNATE_H5
# otherwise fall back to SavedModel folder if present
elif os.path.isdir(SAVED_MODEL_DIR):
    CNN_MODEL_PATH = SAVED_MODEL_DIR
else:
    # nothing exists yet; still point at default so errors report useful path
    CNN_MODEL_PATH = DEFAULT_H5

# Image preprocessing constants
IMAGE_SIZE = (224, 224)  # Target image size for the CNN
NORMALIZED_MEAN = 127.5  # For normalization to [-1, 1] range
NORMALIZED_STD = 127.5

# Global model cache
_model = None


def load_cnn_model():
    """
    Load the pre-trained CNN model from disk (cached).
    
    Returns:
        model: TensorFlow Keras model object, or None if loading fails
    """
    global _model
    
    if _model is not None:
        return _model
    
    try:
        if not os.path.exists(CNN_MODEL_PATH):
            logger.error(f"CNN model not found at {CNN_MODEL_PATH}")
            logger.error("Expected either an HDF5 file or a SavedModel directory")
            logger.error(f"HDF5 file path: {DEFAULT_H5}")
            logger.error(f"SavedModel dir: {SAVED_MODEL_DIR}")
            logger.error("Contents of model folder:")
            if os.path.isdir(MODEL_FOLDER):
                for entry in os.listdir(MODEL_FOLDER):
                    logger.error(f"  - {entry}")
            return None
        
        # If path is a directory, treat as SavedModel; otherwise ensure file isn't empty
        if os.path.isdir(CNN_MODEL_PATH):
            logger.info(f"Loading CNN model from SavedModel directory: {CNN_MODEL_PATH}")
        else:
            file_size = os.path.getsize(CNN_MODEL_PATH)
            if file_size == 0:
                logger.error(f"CNN model file is empty: {CNN_MODEL_PATH}")
                return None
            logger.info(f"Loading CNN model from file: {CNN_MODEL_PATH} (Size: {file_size / 1024 / 1024:.2f}MB)")
        
        # Load with error handling
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if os.path.isdir(CNN_MODEL_PATH):
                # Keras 3 no longer supports legacy SavedModel in load_model; try multiple fallbacks
                logger.info("Detected SavedModel directory, attempting to load")
                from tensorflow import keras as tfkeras
                try:
                    # first attempt: wrap with TFSMLayer
                    logger.info("Trying TFSMLayer wrapper")
                    tfsmlayer = tfkeras.layers.TFSMLayer(CNN_MODEL_PATH, call_endpoint="serving_default")
                    inp = tfkeras.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
                    out = tfsmlayer(inp)
                    _model = tfkeras.Model(inputs=inp, outputs=out)
                except Exception as wrap_err:
                    logger.warning(f"TFSMLayer failed: {wrap_err}")
                    logger.info("Falling back to direct tf.saved_model.load with custom wrapper")
                    # second attempt: load via tf.saved_model.load and create custom predict method
                    import tensorflow as tf
                    loaded = tf.saved_model.load(CNN_MODEL_PATH)
                    signatures = loaded.signatures
                    if 'serving_default' in signatures:
                        infer = signatures['serving_default']
                    else:
                        # take first available
                        infer = list(signatures.values())[0]
                    class SavedModelWrapper:
                        def __init__(self, infer_fn):
                            self._infer = infer_fn
                        def predict(self, x, verbose=0):
                            import tensorflow as tf
                            _x = tf.convert_to_tensor(x)
                            out = self._infer(_x)
                            # return numpy array from first output
                            return list(out.values())[0].numpy()
                    _model = SavedModelWrapper(infer)
            else:
                _model = keras.models.load_model(CNN_MODEL_PATH)
        
        logger.info("CNN model loaded successfully")
        # log shapes if available (wrapper may not have input_shape attr)
        try:
            logger.info(f"Model input shape: {_model.input_shape}")
            logger.info(f"Model output shape: {_model.output_shape}")
        except Exception:
            logger.debug("Unable to log model shapes; object may be a wrapper")
        return _model
    
    except Exception as e:
        logger.error(f"Failed to load CNN model: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None


def preprocess_image(image_path):
    """
    Preprocess ultrasound image for CNN inference.
    
    Steps:
    1. Load image from file path
    2. Convert to RGB (if grayscale)
    3. Resize to 224x224
    4. Normalize pixel values to [-1, 1]
    5. Reshape for batch processing
    
    Args:
        image_path (str): Path to the uploaded ultrasound image file
        
    Returns:
        np.ndarray: Preprocessed image array ready for model prediction,
                   or None if preprocessing fails
    """
    try:
        # Open image and convert to RGB
        image = Image.open(image_path)
        
        # Convert grayscale to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size (224x224)
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        image_array = np.array(image, dtype=np.float32)
        
        # Normalize pixel values from [0, 255] to [-1, 1]
        # This matches typical CNN preprocessing
        image_array = (image_array - NORMALIZED_MEAN) / NORMALIZED_STD
        
        # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
        image_batch = np.expand_dims(image_array, axis=0)
        
        logger.info(f"Image preprocessed successfully: shape={image_batch.shape}")
        return image_batch
    
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return None
    
    except Exception as e:
        logger.error(f"Image preprocessing failed: {str(e)}")
        return None


def predict_ultrasound(image_path):
    """
    Perform PCOS prediction on ultrasound image using CNN.
    
    Args:
        image_path (str): Path to the uploaded ultrasound image
        
    Returns:
        dict: Prediction result containing:
            {
                "success": bool,
                "prediction": "PCOS Likely" or "PCOS Unlikely",
                "probability": float (0-1),
                "confidence": float (0-100 as percentage),
                "error": str (only if success=False)
            }
            
    Example:
        result = predict_ultrasound("/tmp/upload_123.jpg")
        # Output: {
        #   "success": True,
        #   "prediction": "PCOS Likely",
        #   "probability": 0.87,
        #   "confidence": 87.0
        # }
    """
    
    # Load model
    model = load_cnn_model()
    if model is None:
        return {
            "success": False,
            "error": "CNN model failed to load",
            "prediction": None,
            "probability": None,
            "confidence": None
        }
    
    # Preprocess image
    processed_image = preprocess_image(image_path)
    if processed_image is None:
        return {
            "success": False,
            "error": "Image preprocessing failed",
            "prediction": None,
            "probability": None,
            "confidence": None
        }
    
    try:
        # Get model predictions
        # Assuming binary classification (PCOS vs No PCOS)
        # Output shape: (1, 1) or (1, 2) depending on model architecture
        prediction_output = model.predict(processed_image, verbose=0)
        
        # Handle both single output and two-class output
        if prediction_output.shape[-1] == 1:
            # Single output (sigmoid)
            probability = float(prediction_output[0][0])
        else:
            # Two outputs (softmax) - take PCOS class (index 1)
            probability = float(prediction_output[0][1])
        
        # Clamp probability to [0, 1]
        probability = max(0.0, min(1.0, probability))
        
        # Determine prediction label
        prediction_label = "PCOS Likely" if probability >= 0.5 else "PCOS Unlikely"
        
        # Convert to percentage confidence
        confidence = probability * 100
        
        logger.info(f"PCOS prediction: {prediction_label}, confidence: {confidence:.2f}%")
        
        return {
            "success": True,
            "prediction": prediction_label,
            "probability": round(probability, 4),
            "confidence": round(confidence, 2),
            "error": None
        }
    
    except Exception as e:
        logger.error(f"Prediction inference failed: {str(e)}")
        return {
            "success": False,
            "error": f"Inference failed: {str(e)}",
            "prediction": None,
            "probability": None,
            "confidence": None
        }


def combine_predictions(symptom_probability, ultrasound_probability, 
                        symptom_weight=0.6, ultrasound_weight=0.4):
    """
    Combine symptom-based and ultrasound-based predictions for final diagnosis.
    
    Weighted combination:
    final_risk = (symptom_weight * symptom_probability) + 
                 (ultrasound_weight * ultrasound_probability)
    
    Risk stratification:
    - Low Risk: < 40%
    - Moderate Risk: 40-70%
    - High Risk: >= 70%
    
    Args:
        symptom_probability (float): Probability from ensemble model (0-1)
        ultrasound_probability (float): Probability from CNN model (0-1)
        symptom_weight (float): Weight for symptom prediction (default 0.6)
        ultrasound_weight (float): Weight for ultrasound prediction (default 0.4)
        
    Returns:
        dict: Combined prediction with final risk level:
            {
                "final_probability": float (0-1),
                "final_confidence": float (0-100),
                "risk_level": "Low Risk" | "Moderate Risk" | "High Risk",
                "components": {
                    "symptom_probability": float,
                    "ultrasound_probability": float,
                    "symptom_weight": float,
                    "ultrasound_weight": float
                }
            }
    """
    
    # Validate weights sum to approximately 1.0
    total_weight = symptom_weight + ultrasound_weight
    if abs(total_weight - 1.0) > 0.01:
        logger.warning(f"Prediction weights don't sum to 1: {total_weight}")
    
    # Calculate weighted average
    final_probability = (symptom_weight * symptom_probability + 
                        ultrasound_weight * ultrasound_probability)
    
    # Clamp to valid range
    final_probability = max(0.0, min(1.0, final_probability))
    final_confidence = final_probability * 100
    
    # Determine risk level
    if final_probability < 0.4:
        risk_level = "Low Risk"
    elif final_probability < 0.7:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"
    
    logger.info(f"Combined prediction: {risk_level} ({final_confidence:.2f}%)")
    
    return {
        "final_probability": round(final_probability, 4),
        "final_confidence": round(final_confidence, 2),
        "risk_level": risk_level,
        "components": {
            "symptom_probability": round(symptom_probability, 4),
            "ultrasound_probability": round(ultrasound_probability, 4),
            "symptom_weight": symptom_weight,
            "ultrasound_weight": ultrasound_weight
        }
    }
