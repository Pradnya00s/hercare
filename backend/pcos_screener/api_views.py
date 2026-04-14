from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import joblib
import os
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Lazy import for TensorFlow-dependent functions
def get_ultrasound_functions():
    try:
        from .ultrasound_predict import predict_ultrasound, combine_predictions
        return predict_ultrasound, combine_predictions
    except ImportError as e:
        logger.error(f"Failed to import ultrasound prediction functions: {e}")
        return None, None

# Load model and scaler (same logic as your existing view)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "pcos_screener/model/pcos_ensemble_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "pcos_screener/model/scaler.pkl")

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    model = None
    scaler = None
    print("Model loading error:", e)


# IMPORTANT: feature order MUST match training
FEATURE_ORDER = [
    'age_yrs',
    'weight_kg',
    'heightcm',
    'cycleri',
    'cycle_lengthdays',
    'pregnantyn',
    'no_of_abortions',
    'weight_gainyn',
    'hair_growthyn',
    'skin_darkening_yn',
    'hair_lossyn',
    'pimplesyn',
    'fast_food_yn',
    'regexerciseyn'
]


@csrf_exempt
def pcos_form_predict_api(request):
    """
    POST /api/pcos/form-predict/
    Body: JSON
    """
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    if model is None or scaler is None:
        return JsonResponse(
            {"error": "ML model not loaded"},
            status=500
        )

    try:
        data = json.loads(request.body)

        # Collect input features in correct order
        input_values = []
        for feature in FEATURE_ORDER:
            if feature not in data:
                return JsonResponse(
                    {"error": f"Missing field: {feature}"},
                    status=400
                )
            input_values.append(float(data[feature]))

        input_array = np.array(input_values).reshape(1, -1)
        scaled_input = scaler.transform(input_array)

        prediction = int(model.predict(scaled_input)[0])
        probability = float(model.predict_proba(scaled_input)[0][1]) * 100

        response = {
            "prediction": prediction,   # 1 = PCOS, 0 = No PCOS
            "pcos_probability": round(probability, 2),
            "result": (
                "PCOS Likely"
                if prediction == 1
                else "PCOS Unlikely"
            )
        }

        return JsonResponse(response, status=200)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )


@csrf_exempt
def ultrasound_prediction_api(request):
    """
    POST /api/ultrasound/
    
    Upload ultrasound image and receive CNN-based PCOS prediction.
    
    Request:
        - Method: POST (multipart/form-data)
        - Body: file (image) with key 'ultrasound_image'
    
    Response:
        {
            "success": bool,
            "prediction": "PCOS Likely" | "PCOS Unlikely",
            "confidence": float (0-100),
            "probability": float (0-1),
            "error": str (if success=False)
        }
    """
    
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )
    
    # Check if file was uploaded
    if 'ultrasound_image' not in request.FILES:
        return JsonResponse(
            {"error": "No image file provided. Use key 'ultrasound_image'"},
            status=400
        )
    
    uploaded_file = request.FILES['ultrasound_image']
    
    # Validate file size (max 10MB)
    max_file_size = 10 * 1024 * 1024  # 10MB
    if uploaded_file.size > max_file_size:
        return JsonResponse(
            {"error": f"File too large. Maximum size: {max_file_size / 1024 / 1024:.0f}MB"},
            status=400
        )
    
    # Validate file extension
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in allowed_extensions:
        return JsonResponse(
            {"error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"},
            status=400
        )
    
    try:
        # Save uploaded file temporarily
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
        
        logger.info(f"File uploaded and saved: {temp_file_path}")
        
        # Perform CNN prediction on the image
        predict_ultrasound, _ = get_ultrasound_functions()
        if predict_ultrasound is None:
            return JsonResponse(
                {"error": "AI prediction service unavailable"},
                status=503
            )

        prediction_result = predict_ultrasound(temp_file_path)
        
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Temporary file cleaned up: {temp_file_path}")
        
        # Return prediction result
        if prediction_result["success"]:
            response = {
                "success": True,
                "prediction": prediction_result["prediction"],
                "confidence": prediction_result["confidence"],
                "probability": prediction_result["probability"]
            }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": prediction_result["error"]
                },
                status=500
            )
    
    except Exception as e:
        logger.error(f"Ultrasound prediction API error: {str(e)}")
        return JsonResponse(
            {"error": f"Server error: {str(e)}"},
            status=500
        )


@csrf_exempt
def combined_prediction_api(request):
    """
    POST /api/combined-prediction/
    
    Combine symptom-based and ultrasound-based predictions for final diagnosis.
    
    Request:
        {
            "symptom_probability": float (0-1),
            "ultrasound_probability": float (0-1),
            "symptom_weight": float (optional, default 0.6),
            "ultrasound_weight": float (optional, default 0.4)
        }
    
    Response:
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
    
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )
    
    try:
        data = json.loads(request.body)
        
        # Required fields
        if "symptom_probability" not in data or "ultrasound_probability" not in data:
            return JsonResponse(
                {"error": "Missing required fields: symptom_probability, ultrasound_probability"},
                status=400
            )
        
        symptom_prob = float(data["symptom_probability"])
        ultrasound_prob = float(data["ultrasound_probability"])
        
        # Optional weights (use defaults if not provided)
        symptom_weight = float(data.get("symptom_weight", 0.6))
        ultrasound_weight = float(data.get("ultrasound_weight", 0.4))
        
        # Validate probability ranges
        if not (0 <= symptom_prob <= 1):
            return JsonResponse(
                {"error": "symptom_probability must be between 0 and 1"},
                status=400
            )
        if not (0 <= ultrasound_prob <= 1):
            return JsonResponse(
                {"error": "ultrasound_probability must be between 0 and 1"},
                status=400
            )
        
        # Combine predictions
        _, combine_predictions = get_ultrasound_functions()
        if combine_predictions is None:
            return JsonResponse(
                {"error": "Prediction combination service unavailable"},
                status=503
            )

        combined_result = combine_predictions(
            symptom_prob,
            ultrasound_prob,
            symptom_weight,
            ultrasound_weight
        )
        
        return JsonResponse(combined_result, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=400
        )
    
    except ValueError as e:
        return JsonResponse(
            {"error": f"Invalid numeric value: {str(e)}"},
            status=400
        )
    
    except Exception as e:
        logger.error(f"Combined prediction API error: {str(e)}")
        return JsonResponse(
            {"error": f"Server error: {str(e)}"},
            status=500
        )
