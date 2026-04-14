# 🔧 HerCare Development & Extension Guide

## For Developers: Extending HerCare

This guide covers:
- Code structure and architecture
- Running tests
- Modifying and extending features
- Adding new endpoints
- Customizing the UI
- Deploying to production

---

## Architecture Overview

### Backend Architecture

```
Django REST API
├── api_views.py
│   ├── pcos_form_predict_api()      → Symptom prediction
│   ├── ultrasound_prediction_api()  → CNN inference
│   └── combined_prediction_api()    → Weighted combination
├── api_urls.py
│   └── URL routing to views
├── ultrasound_predict.py
│   ├── load_cnn_model()             → Load TensorFlow model
│   ├── preprocess_image()           → Image preprocessing
│   ├── predict_ultrasound()         → CNN prediction
│   └── combine_predictions()        → Combine both models
└── models.py                         → Database models (if needed)
```

### Frontend Architecture

```
React App
├── App.jsx
│   ├── State management (useState)
│   ├── 4-stage workflow
│   └── API integration
├── components/
│   ├── UltrasoundUpload.jsx        → Image upload UI
│   └── UltrasoundUpload.css
└── App.css                          → Main styles
```

---

## Modifying the Symptom Questionnaire

### Current Features (14 symptoms)

Located in: `frontend/src/App.jsx`

```javascript
const [formData, setFormData] = useState({
  age_yrs: "",
  weight_kg: "",
  heightcm: "",
  // ... 11 more fields
});
```

And in `backend/pcos_screener/api_views.py`:

```python
FEATURE_ORDER = [
    'age_yrs',
    'weight_kg',
    'heightcm',
    'cycleri',
    # ... 11 more features (MUST match training data)
]
```

### How to Add a New Question

**Example: Add "Insulin Resistance" question**

#### Step 1: Update Backend Feature List

**File:** `backend/pcos_screener/api_views.py`

```python
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
    'regexerciseyn',
    'insulin_resistanceyn'  # NEW FIELD
]
```

#### Step 2: Update Frontend Form State

**File:** `frontend/src/App.jsx`

```javascript
const [formData, setFormData] = useState({
    age_yrs: "",
    weight_kg: "",
    heightcm: "",
    // ... existing fields
    insulin_resistanceyn: 0  // NEW FIELD
});
```

#### Step 3: Add Form Input

**File:** `frontend/src/App.jsx` → `SymptomForm` component

```jsx
<div className="form-group">
  <label>
    <input
      type="checkbox"
      name="insulin_resistanceyn"
      checked={formData.insulin_resistanceyn === 1}
      onChange={handleInputChange}
    />
    Family History of Insulin Resistance?
  </label>
</div>
```

#### Step 4: Retrain Model (Important!)

⚠️ **Your ML model was trained with 14 features, not 15!**

You must retrain the ensemble model with the new feature:

```python
# train_model.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load training data
df = pd.read_csv('pcos_clean_v1.csv')

# Add new feature if missing (for testing)
if 'insulin_resistanceyn' not in df.columns:
    df['insulin_resistanceyn'] = 0  # Default value

# Define features
features = [
    'age_yrs', 'weight_kg', 'heightcm', 'cycleri',
    'cycle_lengthdays', 'pregnantyn', 'no_of_abortions',
    'weight_gainyn', 'hair_growthyn', 'skin_darkening_yn',
    'hair_lossyn', 'pimplesyn', 'fast_food_yn',
    'regexerciseyn', 'insulin_resistanceyn'  # NEW FEATURE
]

X = df[features]
y = df['PCOS(Y/N)']

# Train model
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_scaled, y)

# Save
joblib.dump(model, 'pcos_ensemble_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
```

---

## Replacing the CNN Model

### Current Model Location
```
backend/pcos_screener/model/model.h5
```

### How to Replace

#### Step 1: Prepare Your New Model

- Must be TensorFlow/Keras compatible
- Input: 224×224×3 ultrasound images
- Output: Binary classification (PCOS / No PCOS)

#### Step 2: Save Model

```python
# your_training_script.py
model = build_and_train_model()  # Your code
model.save('model.h5')  # Must be .h5 format
```

#### Step 3: Update ultrasound_predict.py (if needed)

If your model output format is different:

**File:** `backend/pcos_screener/ultrasound_predict.py`

```python
def predict_ultrasound(image_path):
    # ... existing code ...
    
    # MODIFY THIS SECTION based on your model output
    prediction_output = model.predict(processed_image, verbose=0)
    
    if prediction_output.shape[-1] == 1:
        # Single output (sigmoid)
        probability = float(prediction_output[0][0])
    else:
        # Two outputs (softmax) - adjust index if needed
        probability = float(prediction_output[0][1])
    
    # ... rest of code ...
```

#### Step 4: Test

```bash
cd backend
source venv/bin/activate
python manage.py runserver

# In another terminal
curl -X POST http://127.0.0.1:8000/api/ultrasound/ \
  -F "ultrasound_image=@test_image.jpg"
```

---

## Adding New API Endpoints

### Example: Add "Save Results" Endpoint

**File:** `backend/pcos_screener/api_views.py`

```python
@csrf_exempt
def save_results_api(request):
    """
    POST /api/save-results/
    
    Save prediction results (future: to database)
    """
    
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if "user_email" not in data or "results" not in data:
            return JsonResponse(
                {"error": "Missing: user_email, results"},
                status=400
            )
        
        # TODO: Save to database
        # result_obj = ResultsModel.objects.create(
        #     email=data['user_email'],
        #     results=json.dumps(data['results']),
        #     timestamp=datetime.now()
        # )
        
        return JsonResponse({
            "success": True,
            "message": "Results saved successfully",
            "result_id": "placeholder_id"
        }, status=200)
    
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
```

**File:** `backend/pcos_screener/api_urls.py`

```python
from .api_views import (
    pcos_form_predict_api,
    ultrasound_prediction_api,
    combined_prediction_api,
    save_results_api  # NEW
)

urlpatterns = [
    path("pcos/form-predict/", pcos_form_predict_api),
    path("ultrasound/", ultrasound_prediction_api),
    path("combined-prediction/", combined_prediction_api),
    path("save-results/", save_results_api),  # NEW
]
```

**Frontend:** `frontend/src/App.jsx`

```javascript
const handleSaveResults = async () => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/save-results/",
            {
                user_email: "user@example.com",
                results: {
                    symptom_result: symptomResult,
                    ultrasound_result: ultrasoundResult,
                    final_result: finalResult
                }
            }
        );
        
        console.log("Results saved:", response.data);
    } catch (err) {
        console.error("Save failed:", err);
    }
};
```

---

## Customizing the UI

### Change Color Scheme

**File:** `frontend/src/App.css`

Change the primary gradient color:

```css
/* Before */
.hercare-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* After - Blue theme */
.hercare-header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

/* Also update button colors */
.btn-primary {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
```

### Add Logo

**File:** `frontend/src/App.jsx`

```jsx
function App() {
  return (
    <div className="hercare-container">
      <header className="hercare-header">
        <div className="header-content">
          <img src="/logo.png" alt="HerCare" className="logo" />
          <h1>🏥 HerCare</h1>
          <p>AI-Powered PCOS Screening</p>
        </div>
      </header>
      {/* ... rest of component ... */}
    </div>
  );
}
```

**File:** `frontend/src/App.css`

```css
.logo {
  height: 60px;
  margin-bottom: 1rem;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
```

### Add Dark Mode

```jsx
// In App.jsx
const [darkMode, setDarkMode] = useState(false);

// Toggle button in header
<button onClick={() => setDarkMode(!darkMode)}>
  {darkMode ? '☀️' : '🌙'}
</button>

// Apply class to container
<div className={`hercare-container ${darkMode ? 'dark-mode' : ''}`}>
```

**File:** `frontend/src/App.css`

```css
.hercare-container.dark-mode {
  background-color: #1a1a1a;
  color: white;
}

.hercare-container.dark-mode section {
  background: #2d2d2d;
  color: white;
}
```

---

## Database Integration (Optional)

### Add User History Storage

**File:** `backend/pcos_screener/models.py`

```python
from django.db import models

class PredictionResult(models.Model):
    # User info
    email = models.EmailField()
    
    # Predictions
    symptom_probability = models.FloatField()
    ultrasound_probability = models.FloatField()
    final_probability = models.FloatField()
    risk_level = models.CharField(max_length=20)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.risk_level} ({self.created_at})"
```

### Migrate Database

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

---

## Performance Optimization

### 1. Model Caching

Already implemented in `ultrasound_predict.py`:

```python
_model = None  # Global cache

def load_cnn_model():
    global _model
    if _model is not None:
        return _model  # Return cached model
    _model = keras.models.load_model(CNN_MODEL_PATH)
    return _model
```

### 2. Batch Processing

Add batch endpoint for multiple images:

```python
@csrf_exempt
def batch_ultrasound_prediction_api(request):
    """Process multiple images at once"""
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    
    results = []
    files = request.FILES.getlist('images')
    
    for file in files:
        # Process each file
        result = predict_ultrasound(temp_path)
        results.append(result)
    
    return JsonResponse({"results": results}, status=200)
```

### 3. Compression

Reduce model size:

```python
# During model training
model.save('model_quantized.h5',
           save_format='h5',
           include_optimizer=False)  # Remove optimizer weights
```

---

## Testing

### Backend Unit Tests

**File:** `backend/pcos_screener/tests.py`

```python
from django.test import TestCase
from django.test import Client
import json

class PCSPredictionTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_symptom_prediction_endpoint(self):
        """Test symptom prediction API"""
        payload = {
            "age_yrs": 25,
            "weight_kg": 65,
            "heightcm": 160,
            # ... all 14 features
        }
        
        response = self.client.post(
            '/api/pcos/form-predict/',
            json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('prediction', data)
        self.assertIn('pcos_probability', data)
    
    def test_missing_field(self):
        """Test error handling for missing fields"""
        payload = {"age_yrs": 25}  # Incomplete
        
        response = self.client.post(
            '/api/pcos/form-predict/',
            json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
```

### Run Tests

```bash
cd backend
python manage.py test pcos_screener.tests
```

---

## Logging & Debugging

### Backend Logging

**File:** `backend/hercare_project/settings.py`

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}
```

### Frontend Logging

**File:** `frontend/src/App.jsx`

```javascript
const API_BASE = "http://127.0.0.1:8000";
const DEBUG = true;

const log = (message, data) => {
    if (DEBUG) {
        console.log(`[HerCare] ${message}`, data);
    }
};

// Usage
log("Symptom form submitted", formData);
log("API Response received", response.data);
```

---

## Deployment Checklist

- [ ] Update Django `DEBUG = False`
- [ ] Set `ALLOWED_HOSTS` in settings.py
- [ ] Use environment variables for secrets
- [ ] Configure CORS for production domain
- [ ] Build frontend: `npm run build`
- [ ] Use production-grade server (Gunicorn, etc.)
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure database (PostgreSQL for production)
- [ ] Set up monitoring/logging
- [ ] Test all endpoints before deployment

---

## Useful Commands Reference

```bash
# Backend
python manage.py runserver              # Start dev server
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations
python manage.py shell                  # Django interactive shell
python manage.py test                   # Run tests

# Frontend
npm run dev                              # Start dev server
npm run build                            # Build for production
npm run preview                          # Preview production build
npm run lint                             # Run ESLint

# Git
git status                              # Check status
git add .                               # Stage changes
git commit -m "message"                 # Commit
git push origin main                    # Push to repository
```

---

## Troubleshooting Development

### Hot Reload Not Working

```bash
# Frontend hot reload issues
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Model Not Updating

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Restart server
python manage.py runserver
```

### API Changes Not Reflected

```bash
# Browser cache issue
# Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

# Or clear browser cache manually
```

---

## Code Style & Best Practices

### Python (Backend)

- Use type hints
- Document functions with docstrings
- Follow PEP 8 style guide
- Use meaningful variable names

### JavaScript (Frontend)

- Use const/let (avoid var)
- Use arrow functions
- Component names in PascalCase
- Keep components under 300 lines

---

## Next Steps for Enhancement

1. **Add User Authentication** → JWT tokens, user accounts
2. **Database Storage** → Save results, build history
3. **Advanced Analytics** → Charts, trends, statistics
4. **Mobile App** → React Native version
5. **Multi-language Support** → i18n integration
6. **Email Notifications** → Send results via email
7. **Doctor Integration** → Share results with healthcare providers
8. **Continuous Learning** → Model retraining pipeline

---

**Happy developing! 🚀**
