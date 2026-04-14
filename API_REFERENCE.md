# API Reference – HerCare Backend

## Complete API Documentation

All API endpoints are exposed via Django REST Framework.

---

## Base URL

```
http://127.0.0.1:8000/api/
```

---

## Endpoints

### 1. Symptom-Based PCOS Prediction

**Endpoint:** `POST /api/pcos/form-predict/`

**Description:** Analyzes symptom data and returns PCOS risk prediction using the ensemble classifier.

#### Request

**Content-Type:** `application/json`

**Body Parameters:**

| Parameter | Type | Required | Range/Format | Example |
|-----------|------|----------|--------------|---------|
| age_yrs | number | Yes | 18-100 | 25 |
| weight_kg | number | Yes | 30-200 | 65 |
| heightcm | number | Yes | 100-250 | 160 |
| cycleri | integer | Yes | 0 or 1 | 1 |
| cycle_lengthdays | number | Yes | 20-90 | 45 |
| pregnantyn | integer | Yes | 0 or 1 | 0 |
| no_of_abortions | integer | Yes | 0-10 | 0 |
| weight_gainyn | integer | Yes | 0 or 1 | 1 |
| hair_growthyn | integer | Yes | 0 or 1 | 1 |
| skin_darkening_yn | integer | Yes | 0 or 1 | 1 |
| hair_lossyn | integer | Yes | 0 or 1 | 0 |
| pimplesyn | integer | Yes | 0 or 1 | 1 |
| fast_food_yn | integer | Yes | 0 or 1 | 1 |
| regexerciseyn | integer | Yes | 0 or 1 | 0 |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/pcos/form-predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "age_yrs": 25,
    "weight_kg": 65,
    "heightcm": 160,
    "cycleri": 1,
    "cycle_lengthdays": 45,
    "pregnantyn": 0,
    "no_of_abortions": 0,
    "weight_gainyn": 1,
    "hair_growthyn": 1,
    "skin_darkening_yn": 1,
    "hair_lossyn": 0,
    "pimplesyn": 1,
    "fast_food_yn": 1,
    "regexerciseyn": 0
  }'
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "prediction": 1,
  "pcos_probability": 62.50,
  "result": "PCOS Likely"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| prediction | integer | 1 = PCOS detected, 0 = No PCOS |
| pcos_probability | number | Risk percentage (0-100) |
| result | string | "PCOS Likely" or "PCOS Unlikely" |

#### Error Responses

**Missing Field (Status 400):**
```json
{
  "error": "Missing field: age_yrs"
}
```

**Invalid JSON (Status 400):**
```json
{
  "error": "Invalid JSON format"
}
```

**Model Not Loaded (Status 500):**
```json
{
  "error": "ML model not loaded"
}
```

**Server Error (Status 500):**
```json
{
  "error": "Internal server error message"
}
```

---

### 2. Ultrasound Image Analysis

**Endpoint:** `POST /api/ultrasound/`

**Description:** Uploads ultrasound image and returns CNN-based PCOS prediction.

#### Request

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Format | Max Size | Notes |
|-----------|------|----------|--------|----------|-------|
| ultrasound_image | file | Yes | JPEG, PNG, GIF, BMP | 10MB | Ultrasound scan image |

#### Example Request

```bash
# Using curl
curl -X POST http://127.0.0.1:8000/api/ultrasound/ \
  -F "ultrasound_image=@/path/to/image.jpg"

# Using Python requests
import requests

with open('ultrasound.jpg', 'rb') as f:
    files = {'ultrasound_image': f}
    response = requests.post(
        'http://127.0.0.1:8000/api/ultrasound/',
        files=files
    )
    print(response.json())

# Using JavaScript/Fetch
const formData = new FormData();
formData.append('ultrasound_image', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/ultrasound/', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "success": true,
  "prediction": "PCOS Likely",
  "confidence": 87.50,
  "probability": 0.875
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | True if prediction successful |
| prediction | string | "PCOS Likely" or "PCOS Unlikely" |
| confidence | number | Confidence percentage (0-100) |
| probability | number | Confidence as decimal (0-1) |

#### Error Responses

**No File Provided (Status 400):**
```json
{
  "error": "No image file provided. Use key 'ultrasound_image'"
}
```

**File Too Large (Status 400):**
```json
{
  "error": "File too large. Maximum size: 10MB"
}
```

**Invalid File Type (Status 400):**
```json
{
  "error": "Invalid file type. Allowed: jpg, jpeg, png, gif, bmp"
}
```

**Image Processing Failed (Status 500):**
```json
{
  "success": false,
  "error": "Image preprocessing failed"
}
```

**Model Not Available (Status 500):**
```json
{
  "success": false,
  "error": "CNN model failed to load"
}
```

---

### 3. Combined Prediction

**Endpoint:** `POST /api/combined-prediction/`

**Description:** Combines symptom and ultrasound predictions using weighted average for final diagnosis.

#### Request

**Content-Type:** `application/json`

**Body Parameters:**

| Parameter | Type | Required | Range | Default | Description |
|-----------|------|----------|-------|---------|-------------|
| symptom_probability | number | Yes | 0-1 | - | Symptom risk as decimal (divide by 100) |
| ultrasound_probability | number | Yes | 0-1 | - | Ultrasound risk as decimal (divide by 100) |
| symptom_weight | number | No | 0-1 | 0.6 | Weight for symptom prediction |
| ultrasound_weight | number | No | 0-1 | 0.4 | Weight for ultrasound prediction |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/combined-prediction/ \
  -H "Content-Type: application/json" \
  -d '{
    "symptom_probability": 0.625,
    "ultrasound_probability": 0.875,
    "symptom_weight": 0.6,
    "ultrasound_weight": 0.4
  }'
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "final_probability": 0.72,
  "final_confidence": 72.00,
  "risk_level": "High Risk",
  "components": {
    "symptom_probability": 0.625,
    "ultrasound_probability": 0.875,
    "symptom_weight": 0.6,
    "ultrasound_weight": 0.4
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| final_probability | number | Combined risk (0-1) |
| final_confidence | number | Combined confidence (0-100) |
| risk_level | string | "Low Risk", "Moderate Risk", or "High Risk" |
| components | object | Breakdown of calculation |

**Risk Level Breakdown:**

- **Low Risk**: final_probability < 0.4 (< 40%)
- **Moderate Risk**: 0.4 ≤ final_probability < 0.7 (40-70%)
- **High Risk**: final_probability ≥ 0.7 (≥ 70%)

#### Error Responses

**Missing Required Fields (Status 400):**
```json
{
  "error": "Missing required fields: symptom_probability, ultrasound_probability"
}
```

**Invalid Probability Range (Status 400):**
```json
{
  "error": "symptom_probability must be between 0 and 1"
}
```

**Invalid JSON (Status 400):**
```json
{
  "error": "Invalid JSON format"
}
```

**Server Error (Status 500):**
```json
{
  "error": "Server error: internal message"
}
```

---

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Request successful, data returned |
| 400 | Bad Request | Missing/invalid parameters |
| 405 | Method Not Allowed | Wrong HTTP method (e.g., GET instead of POST) |
| 415 | Unsupported Media Type | Wrong Content-Type header |
| 500 | Internal Server Error | Server-side error, model loading failed |

---

## Request/Response Examples

### Complete Workflow Example

#### Step 1: Get Symptom Prediction

```bash
# Request
POST /api/pcos/form-predict/
{
  "age_yrs": 28,
  "weight_kg": 72,
  "heightcm": 162,
  "cycleri": 1,
  "cycle_lengthdays": 50,
  "pregnantyn": 0,
  "no_of_abortions": 0,
  "weight_gainyn": 1,
  "hair_growthyn": 1,
  "skin_darkening_yn": 0,
  "hair_lossyn": 1,
  "pimplesyn": 1,
  "fast_food_yn": 1,
  "regexerciseyn": 1
}

# Response
{
  "prediction": 1,
  "pcos_probability": 75.30,
  "result": "PCOS Likely"
}
```

#### Step 2: Upload Ultrasound Image

```bash
# Request
POST /api/ultrasound/
Form Data: ultrasound_image=<file>

# Response
{
  "success": true,
  "prediction": "PCOS Likely",
  "confidence": 82.40,
  "probability": 0.824
}
```

#### Step 3: Get Combined Prediction

```bash
# Request
POST /api/combined-prediction/
{
  "symptom_probability": 0.753,
  "ultrasound_probability": 0.824,
  "symptom_weight": 0.6,
  "ultrasound_weight": 0.4
}

# Response
{
  "final_probability": 0.78,
  "final_confidence": 78.40,
  "risk_level": "High Risk",
  "components": {
    "symptom_probability": 0.753,
    "ultrasound_probability": 0.824,
    "symptom_weight": 0.6,
    "ultrasound_weight": 0.4
  }
}
```

---

## Integration Guide

### Python Integration

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def get_symptom_prediction(data):
    """Get PCOS prediction from symptoms"""
    response = requests.post(
        f"{BASE_URL}/pcos/form-predict/",
        json=data
    )
    return response.json()

def upload_ultrasound(image_path):
    """Upload ultrasound image and get prediction"""
    with open(image_path, 'rb') as f:
        files = {'ultrasound_image': f}
        response = requests.post(
            f"{BASE_URL}/ultrasound/",
            files=files
        )
    return response.json()

def get_combined_prediction(symptom_prob, ultrasound_prob):
    """Get combined prediction"""
    data = {
        "symptom_probability": symptom_prob,
        "ultrasound_probability": ultrasound_prob
    }
    response = requests.post(
        f"{BASE_URL}/combined-prediction/",
        json=data
    )
    return response.json()

# Usage
symptom_data = {
    "age_yrs": 25,
    "weight_kg": 65,
    # ... all 14 features
}

symptom_result = get_symptom_prediction(symptom_data)
print(f"Symptom Risk: {symptom_result['pcos_probability']}%")

ultrasound_result = upload_ultrasound("image.jpg")
print(f"Ultrasound Confidence: {ultrasound_result['confidence']}%")

final_result = get_combined_prediction(
    symptom_result['pcos_probability'] / 100,
    ultrasound_result['probability']
)
print(f"Final Risk Level: {final_result['risk_level']}")
```

### JavaScript/Fetch Integration

```javascript
const API_BASE = 'http://127.0.0.1:8000/api';

async function getSymptomPrediction(formData) {
  const response = await fetch(
    `${API_BASE}/pcos/form-predict/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    }
  );
  return response.json();
}

async function uploadUltrasound(imageFile) {
  const formData = new FormData();
  formData.append('ultrasound_image', imageFile);
  
  const response = await fetch(
    `${API_BASE}/ultrasound/`,
    { method: 'POST', body: formData }
  );
  return response.json();
}

async function getCombinedPrediction(symptomProb, ultrasoundProb) {
  const response = await fetch(
    `${API_BASE}/combined-prediction/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        symptom_probability: symptomProb,
        ultrasound_probability: ultrasoundProb
      })
    }
  );
  return response.json();
}

// Usage
const symptomResult = await getSymptomPrediction(formData);
const ultrasoundResult = await uploadUltrasound(imageFile);
const finalResult = await getCombinedPrediction(
  symptomResult.pcos_probability / 100,
  ultrasoundResult.probability
);
```

---

## Rate Limiting & Performance

| Operation | Typical Duration | Optimization |
|-----------|------------------|--------------|
| Symptom prediction | 50-100ms | Model cached in memory |
| Ultrasound prediction | 1-3 seconds | Model cached, first call slower |
| Combined prediction | 10-20ms | Lightweight computation |
| Image upload | Variable | Depends on file size and network |

---

## Security Headers

For production, add these headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

---

## CORS Headers

For frontend on different domain:

```
Access-Control-Allow-Origin: http://your-frontend-url
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
Access-Control-Max-Age: 86400
```

---

## Authentication (Future)

When JWT authentication is added:

```bash
# Get token
POST /auth/token/
{
  "email": "user@example.com",
  "password": "password"
}

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Use token in requests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

**For questions or issues, refer to WALKTHROUGH.md or DEVELOPMENT.md**
