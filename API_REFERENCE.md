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

## Authentication Endpoints

### 1. Register New User

**Endpoint:** `POST /api/auth/register/`

**Description:** Create a new user account

#### Request

**Content-Type:** `application/json`

**Body Parameters:**

| Parameter | Type | Required | Format | Example |
|-----------|------|----------|--------|---------|
| first_name | string | Yes | Max 150 chars | Jane |
| last_name | string | Yes | Max 150 chars | Doe |
| email | string | Yes | Valid email | jane@example.com |
| password | string | Yes | Min 8 chars | SecurePass123 |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "password": "SecurePass123"
  }'
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "id": 1,
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "message": "Account created successfully"
}
```

#### Error Responses

**Email Already Exists (Status 400):**
```json
{
  "error": "Email already registered"
}
```

**Invalid Email (Status 400):**
```json
{
  "error": "Invalid email format"
}
```

**Weak Password (Status 400):**
```json
{
  "error": "Password must be at least 8 characters"
}
```

---

### 2. User Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and receive JWT tokens

#### Request

**Content-Type:** `application/json`

**Body Parameters:**

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| email | string | Yes | jane@example.com |
| password | string | Yes | SecurePass123 |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "SecurePass123"
  }'
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| access | string | JWT access token (15 min expiry) |
| refresh | string | JWT refresh token (7 day expiry) |
| user | object | User profile data |

#### Error Responses

**Invalid Credentials (Status 401):**
```json
{
  "error": "Invalid email or password"
}
```

**User Not Found (Status 404):**
```json
{
  "error": "User account not found"
}
```

---

### 3. Get User Profile

**Endpoint:** `GET /api/auth/profile/`

**Description:** Retrieve authenticated user's profile

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

#### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "id": 1,
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "date_joined": "2026-04-14T10:30:00Z"
}
```

#### Error Responses

**Unauthorized (Status 401):**
```json
{
  "error": "Authentication credentials were not provided"
}
```

**Token Expired (Status 401):**
```json
{
  "error": "Token is invalid or expired"
}
```

---

## Dashboard Endpoints

### 1. Get User Dashboard

**Endpoint:** `GET /api/dashboard/`

**Description:** Get user's health dashboard with screening history

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

#### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "user": {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "latest_screening": {
    "date": "2026-04-14",
    "risk_level": "Moderate RIsk",
    "confidence": 65.50
  },
  "screening_history": [
    {
      "id": 1,
      "date": "2026-04-14",
      "risk_level": "Moderate Risk",
      "confidence": 65.50
    }
  ],
  "total_screenings": 1
}
```

---

## Period Tracker Endpoints

### 1. Add Menstrual Cycle

**Endpoint:** `POST /api/period-tracker/cycle/`

**Description:** Log a new menstrual cycle

#### Request

**Content-Type:** `application/json`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Body Parameters:**

| Parameter | Type | Required | Format | Example |
|-----------|------|----------|--------|---------|
| start_date | string | Yes | YYYY-MM-DD | 2026-04-01 |
| end_date | string | Yes | YYYY-MM-DD | 2026-04-05 |
| cycle_length | integer | No | Days | 28 |
| period_length | integer | No | Days | 5 |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/period-tracker/cycle/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2026-04-01",
    "end_date": "2026-04-05",
    "cycle_length": 28,
    "period_length": 5
  }'
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "id": 1,
  "start_date": "2026-04-01",
  "end_date": "2026-04-05",
  "cycle_length": 28,
  "created_at": "2026-04-14T10:30:00Z"
}
```

---

### 2. Log Daily Symptoms

**Endpoint:** `POST /api/period-tracker/symptoms/`

**Description:** Log daily period symptoms

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

**Body Parameters:**

| Parameter | Type | Example |
|-----------|------|---------|
| date | string | 2026-04-05 |
| flow | string | Medium |
| cramps | boolean | true |
| fatigue | boolean | true |
| acne | boolean | false |
| headache | boolean | false |
| bloating | boolean | true |
| breast_tenderness | boolean | true |
| mood | string | Happy, Calm |
| notes | string | Feeling better |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/period-tracker/symptoms/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-05",
    "flow": "Medium",
    "cramps": true,
    "fatigue": true,
    "acne": false,
    "headache": false,
    "bloating": true,
    "breast_tenderness": true,
    "mood": "Happy, Calm",
    "notes": "Feeling better"
  }'
```

#### Success Response

**Status Code:** `201 Created`

```json
{
  "id": 1,
  "date": "2026-04-05",
  "flow": "Medium",
  "cramps": true,
  "fatigue": true,
  "created_at": "2026-04-05T09:00:00Z"
}
```

---

### 3. Get Cycle Prediction

**Endpoint:** `GET /api/period-tracker/predict/`

**Description:** Get predicted next period and ovulation window

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

#### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/period-tracker/predict/ \
  -H "Authorization: Bearer {token}"
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "predicted_start_date": "2026-05-01",
  "avg_cycle_length": 28.5,
  "ovulation_day": "2026-04-17",
  "fertile_window_start": "2026-04-15",
  "fertile_window_end": "2026-04-19",
  "confidence": "medium"
}
```

---

### 4. Get Symptom Patterns

**Endpoint:** `GET /api/period-tracker/patterns/`

**Description:** Detect recurring symptom patterns

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

#### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/period-tracker/patterns/ \
  -H "Authorization: Bearer {token}"
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "patterns": [
    "Frequent cramps detected",
    "Frequent fatigue detected",
    "Frequent bloating detected"
  ],
  "total_logs": 5,
  "analysis_period": "last 30 days"
}
```

---

## AI Health Companion Endpoints

### 1. Send Chat Message

**Endpoint:** `POST /api/chatbot/message/`

**Description:** Send message to AI health companion powered by Google Gemini

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body Parameters:**

| Parameter | Type | Required | Example |
|-----------|------|----------|---------|
| message | string | Yes | What are symptoms of PCOS? |
| language | string | No (default: en) | en, es, fr |

#### Example Request

```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/message/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are symptoms of PCOS?",
    "language": "en"
  }'
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "user_message": "What are symptoms of PCOS?",
  "ai_response": "PCOS (Polycystic Ovary Syndrome) symptoms include: irregular periods, excess androgen, hair growth, acne, pelvic pain...",
  "timestamp": "2026-04-14T14:30:00Z",
  "language": "en"
}
```

#### Error Responses

**Missing API Key (Status 500):**
```json
{
  "error": "AI service not configured. Missing GEMINI_API_KEY"
}
```

**API Error (Status 500):**
```json
{
  "error": "AI service temporarily unavailable"
}
```

---

### 2. Get Chat History

**Endpoint:** `GET /api/chatbot/history/`

**Description:** Retrieve user's chat history

#### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

#### Example Request

```bash
curl -X GET http://127.0.0.1:8000/api/chatbot/history/ \
  -H "Authorization: Bearer {token}"
```

#### Success Response

**Status Code:** `200 OK`

```json
{
  "messages": [
    {
      "id": 1,
      "user_message": "What is PCOS?",
      "ai_response": "PCOS is a hormonal disorder...",
      "timestamp": "2026-04-14T10:00:00Z"
    },
    {
      "id": 2,
      "user_message": "How is it treated?",
      "ai_response": "PCOS treatment includes...",
      "timestamp": "2026-04-14T10:15:00Z"
    }
  ],
  "total_messages": 2
}
```

---

## Error Handling

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

## Complete Authenticated Workflow Example

### Step 1: Register User

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "password": "SecurePass123"
  }'

# Response: {"id": 1, "email": "jane@example.com", "message": "Account created"}
```

### Step 2: Login & Get Tokens

```bash
RESPONSE=$(curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "SecurePass123"
  }')

TOKEN=$(echo $RESPONSE | jq -r '.access')
```

### Step 3: Get Dashboard

```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer $TOKEN"
```

### Step 4: PCOS Screening

```bash
# Step 4a: Get Symptom Prediction
curl -X POST http://127.0.0.1:8000/api/pcos/form-predict/ \
  -H "Authorization: Bearer $TOKEN" \
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

# Response: {"prediction": 1, "pcos_probability": 62.50, "result": "PCOS Likely"}
```

### Step 5: Period Tracking

```bash
# Log a cycle
curl -X POST http://127.0.0.1:8000/api/period-tracker/cycle/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2026-04-01",
    "end_date": "2026-04-05",
    "cycle_length": 28
  }'

# Get predictions
curl -X GET http://127.0.0.1:8000/api/period-tracker/predict/ \
  -H "Authorization: Bearer $TOKEN"
```

### Step 6: AI Health Chat

```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/message/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of PCOS?",
    "language": "en"
  }'

# Response: {"user_message": "...", "ai_response": "PCOS symptoms include..."}
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
