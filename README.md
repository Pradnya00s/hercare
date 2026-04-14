# 🏥 HerCare – AI-Powered PCOS Screening Platform

## Overview

**HerCare** is a comprehensive full-stack AI healthcare application designed to empower women with intelligent health management. The platform combines advanced PCOS screening with period tracking and AI-powered health guidance:

1. **User Authentication System** – Secure registration and login with JWT tokens
2. **Personalized Dashboard** – User health overview and screening history
3. **Two-Stage PCOS Prediction** – Machine learning ensemble (14 health indicators) + CNN ultrasound analysis
4. **Period Tracker** – Menstrual cycle prediction, ovulation window calculation, and symptom pattern detection
5. **AI Health Companion** – Real-time health guidance powered by Google Gemini API
6. **Modern React Frontend** – Intuitive multi-step workflow with responsive healthcare-focused design

This integrated approach delivers personalized health insights with seamless user experience.

---

## 🎯 Key Features

✅ **Secure User Authentication**
- Email-based registration and login
- JWT token-based session management
- Protected routes and API endpoints
- Password validation and security

✅ **Personalized Health Dashboard**
- User profile management
- Health summary and screening history
- Quick access to PCOS screening
- Responsive design for all devices

✅ **Two-Stage PCOS Prediction**
- Comprehensive symptom questionnaire (14 health indicators)
- CNN-based ultrasound image analysis
- Intelligent weighted prediction combination
- Risk stratification (Low/Moderate/High)
- Result persistence and history tracking

✅ **Period & Cycle Management**
- Menstrual cycle tracking and prediction
- Ovulation window calculation
- Symptom logging (6 symptoms per day)
- Recurring pattern detection
- Lifestyle monitoring (sleep, stress, activity levels)

✅ **AI Health Companion**
- Real-time health chatbot powered by Ollama
- Medically responsible responses
- Multi-language support
- Personalized health guidance

✅ **Modern User Interface**
- React 19 with React Router
- Healthcare-focused lavender theme
- Multi-step guided workflow
- Real-time validation and feedback

✅ **Secure & Scalable**
- Django REST API with authentication
- File upload validation and security
- Comprehensive error handling
- Production-ready architecture

---

## 🏗️ Project Structure

```
HerCare/
├── backend/                          # Django REST API
│   ├── manage.py
│   ├── requirements.txt              # Python dependencies
│   ├── db.sqlite3                    # SQLite database
│   ├── hercare_project/              # Django configuration
│   │   ├── settings.py               # Project settings (JWT, CORS, apps)
│   │   ├── urls.py                   # Main URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/                     # User authentication app (NEW)
│   │   ├── models.py                 # CustomUser model (email login)
│   │   ├── serializers.py            # Auth serializers (register/login)
│   │   ├── views.py                  # Auth endpoints (register/login/profile)
│   │   ├── urls.py                   # Auth routes
│   │   ├── admin.py                  # Admin interface
│   │   ├── apps.py                   # App configuration
│   │   └── migrations/               # Database migrations
│   ├── dashboard/                    # User dashboard app (NEW)
│   │   ├── views.py                  # Dashboard endpoint
│   │   ├── urls.py                   # Dashboard routes
│   │   ├── admin.py                  # Admin interface
│   │   ├── apps.py                   # App configuration
│   │   └── migrations/               # Database migrations
│   ├── pcos_screener/                # PCOS screening app
│   │   ├── models.py                 # PCOSScreener model
│   │   ├── api_views.py              # PCOS prediction endpoints
│   │   ├── api_urls.py               # PCOS API routes
│   │   ├── ultrasound_predict.py     # CNN inference & preprocessing
│   │   ├── ml_preprocess.py          # ML preprocessing utilities
│   │   ├── data/                     # Training datasets
│   │   │   └── pcos_clean_v1.csv     # Historical PCOS patient data
│   │   ├── model/                    # Pre-trained ML models
│   │   │   ├── pcosmodel.h5          # CNN model (TensorFlow/Keras)
│   │   │   └── pcos_ultrasound_model/# SavedModel format
│   │   ├── migrations/
│   │   ├── templates/
│   │   └── static/
│   ├── period_tracker/               # Menstrual cycle tracking app
│   │   ├── models.py                 # Cycle, SymptomLog, LifestyleLog models
│   │   ├── services.py               # Cycle prediction & pattern detection
│   │   ├── views.py                  # Tracker endpoints
│   │   ├── urls.py                   # Tracker routes
│   │   ├── ml_model.py               # Irregularity prediction
│   │   └── migrations/               # Database migrations
│   ├── chatbot/                      # AI Health companion app
│   │   ├── models.py                 # ChatMessage model
│   │   ├── services.py               # Google Gemini API integration
│   │   ├── views.py                  # Chat endpoints
│   │   ├── urls.py                   # Chat routes
│   │   └── migrations/               # Database migrations
│   └── venv/                         # Python virtual environment
│
└── frontend/                         # React + Vite (NEW)
    ├── package.json                  # Node dependencies
    ├── vite.config.js                # Vite configuration
    ├── index.html                    # Main HTML template
    ├── src/
    │   ├── main.jsx                  # React entry point
    │   ├── App.jsx                   # Main app with React Router
    │   ├── App.css                   # Global styles (healthcare theme)
    │   ├── index.css                 # Base styles
    │   ├── services/
    │   │   └── api.js                # API service with JWT interceptors
    │   ├── components/               # Reusable React components
    │   │   ├── Navbar.jsx/css        # Navigation bar with auth state
    │   │   ├── UploadBox.jsx/css     # File upload component
    │   │   ├── SymptomToggle.jsx/css # Symptom selection toggles
    │   │   └── ResultCard.jsx/css    # Results display card
    │   └── pages/                    # React pages
    │       ├── Home.jsx/css          # Landing page
    │       ├── Auth.jsx/css          # Login/register shared page
    │       ├── Dashboard.jsx/css     # User dashboard
    │       ├── PCOSDetector.jsx/css  # PCOS screening workflow
    │       ├── PeriodTracker.jsx/css # Menstrual cycle tracker
    │       ├── AIHealth.jsx/css      # AI-assisted health features
    │       ├── Onboarding.jsx/css    # New user onboarding
    │       └── Profile.jsx/css       # User profile page
    ├── public/                       # Static assets
    └── node_modules/                 # Node dependencies
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **pip** (Python package manager)
- **npm** (Node package manager)

### Setup in 6 Steps

#### 1️⃣ **Clone & Navigate**
```bash
cd HerCare
```

#### 2️⃣ **Setup Backend**
```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes Django, DRF, JWT, TensorFlow, etc.)
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start Django server
python manage.py runserver
# Server runs at http://127.0.0.1:8000
```

#### 3️⃣ **Setup Frontend** (new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend runs at http://localhost:5173
```

#### 4️⃣ **Access Application**
Open browser → http://localhost:5173

#### 5️⃣ **Create Account & Test**
- Register a new account
- Login to access dashboard
- Complete PCOS screening workflow

#### 6️⃣ **Test Full Workflow**
- Register → Login → Dashboard
- Complete symptom questionnaire
- Upload ultrasound image
- View combined diagnosis results

---

## 🔐 Authentication System

HerCare uses JWT (JSON Web Tokens) for secure authentication:

- **Registration**: Email-based user accounts
- **Login**: Email + password authentication
- **Token Management**: Access tokens (15 min) + refresh tokens (7 days)
- **Protected Routes**: All PCOS endpoints require authentication
- **Auto-refresh**: Frontend automatically refreshes expired tokens

### User Model
- Custom user model extending Django's AbstractUser
- Email as primary login field (instead of username)
- First name, last name, email, password fields
- Date joined tracking

---

## 📋 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

Request Body:
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "password": "securepassword123"
}

Response:
{
  "user": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
  },
  "message": "User registered successfully"
}
```

#### Login User
```http
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

Request Body:
{
  "email": "jane.doe@example.com",
  "password": "securepassword123"
}

Response:
{
  "user": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Get User Profile
```http
GET http://127.0.0.1:8000/api/auth/profile/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### Dashboard Endpoints

#### Get User Dashboard
```http
GET http://127.0.0.1:8000/api/dashboard/
Authorization: Bearer <access_token>

Response:
{
  "user": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
  },
  "last_pcos_result": {
    "date": "2024-01-15",
    "result": "Low Risk"
  }
}
```

---

## 🔧 Configuration

### Backend Settings (`backend/hercare_project/settings.py`)

**Authentication Configuration:**
```python
# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# JWT settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```

### Frontend API Configuration (`frontend/src/services/api.js`)

```javascript
// Base URL includes /api because the frontend service uses the backend API prefix.
const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));
```

---

## 📊 Data & Models

### Symptom Features (6 key indicators)

| Feature | Type | Description |
|---------|------|-------------|
| irregular_periods | Boolean | Irregular menstrual cycles |
| weight_gain | Boolean | Sudden weight gain |
| acne | Boolean | Acne or skin issues |
| hair_loss | Boolean | Hair loss |
| fatigue | Boolean | Chronic fatigue |
| mood_changes | Boolean | Mood changes |

### Machine Learning Models

#### 1. Symptom Analysis Model
- **Type**: Scikit-learn ensemble classifier
- **Input**: 6 symptom boolean features
- **Output**: PCOS probability score
- **Training**: Based on medical datasets

#### 2. CNN Ultrasound Model
- **Type**: TensorFlow/Keras convolutional neural network
- **Input**: 224×224×3 ultrasound images
- **Output**: PCOS detection probability
- **Architecture**: Medical image analysis CNN

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Test authentication endpoints
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"testpass123"}'

# Test protected endpoints (replace TOKEN with actual JWT)
curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:8000/api/dashboard/
```

### Frontend Testing

```bash
cd frontend

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)
- **Django** 4.2.11 – Web framework
- **djangorestframework** 3.14.0 – REST API toolkit
- **djangorestframework-simplejwt** 5.3.0 – JWT authentication
- **django-cors-headers** 4.3.1 – CORS support
- **tensorflow** 2.16.1 – Deep learning framework
- **scikit-learn** 1.4.1 – Machine learning library
- **Pillow** 10.1.0 – Image processing

### Frontend (`package.json`)
- **React** 19.2.0 – UI library
- **react-router-dom** 6.26.1 – Routing
- **axios** 1.13.6 – HTTP client
- **Vite** 7.2.4 – Build tool

---

## 🔒 Security Features

✅ **Authentication & Authorization**
- JWT token-based authentication
- Protected API endpoints
- Secure password handling
- Session management

✅ **File Upload Security**
- MIME type validation
- File size limits (10MB max)
- Secure temporary file handling
- Automatic cleanup

✅ **Data Protection**
- No sensitive data stored long-term
- Uploaded images processed and deleted
- HTTPS ready for production

---

## 🚨 Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Module not found: tensorflow` | TensorFlow not installed | Install with `pip install tensorflow` |
| `Authentication failed` | Invalid JWT token | Check token expiration, re-login |
| `CORS error` | Frontend/backend mismatch | Update CORS settings in settings.py |
| `File upload failed` | Invalid file format/size | Use JPEG/PNG < 10MB |
| `Database connection failed` | PostgreSQL not configured | Use SQLite for development |

---

## 🔄 Application Workflow

```
┌─────────────────┐
│   Landing Page  │
│   (HerCare)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   User Registration  │
│   or Login       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│   (Health Overview) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PCOS Detector │
│   (3-Step Process) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────┐
│ Step 1│  │ Step 2│
│ Symptoms│  │Ultrasound│
└──────┘  └──────┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│   Step 3: Results│
│   (AI Analysis)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │
│   (Updated)     │
└─────────────────┘
```

---

## 📚 Documentation Files

- **[WALKTHROUGH.md](./WALKTHROUGH.md)** – Step-by-step setup and usage guide
- **[API_REFERENCE.md](./API_REFERENCE.md)** – Detailed API documentation
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** – Development setup and contribution guidelines

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: HerCare is a screening tool for informational purposes only and should **NOT** be considered a medical diagnosis.

- Results are AI-powered predictions, not clinical diagnoses
- Always consult qualified healthcare professionals for proper evaluation
- This tool supplements, not replaces, professional medical consultation
- Users assume full responsibility for decisions based on results

---

## 🎉 What's Next?

- ✅ Complete authentication system implemented
- ✅ Modern React frontend with routing
- ✅ Two-stage PCOS prediction workflow
- 🔄 Model retraining pipeline (future)
- 📊 Advanced analytics dashboard (future)
- 🌍 Multi-language support (future)
- ☁️ Cloud deployment (AWS/Azure) (future)

---

**Built with ❤️ for women's health**

---

---

## 📊 Data Preprocessing

### Symptom Features (14 input variables)

| Feature | Type | Range |
|---------|------|-------|
| age_yrs | Numeric | 18-50 |
| weight_kg | Numeric | 40-150 |
| heightcm | Numeric | 140-200 |
| cycleri | Binary | 0/1 |
| cycle_lengthdays | Numeric | 20-90 |
| pregnantyn | Binary | 0/1 |
| no_of_abortions | Numeric | 0-10 |
| weight_gainyn | Binary | 0/1 |
| hair_growthyn | Binary | 0/1 |
| skin_darkening_yn | Binary | 0/1 |
| hair_lossyn | Binary | 0/1 |
| pimplesyn | Binary | 0/1 |
| fast_food_yn | Binary | 0/1 |
| regexerciseyn | Binary | 0/1 |

**Preprocessing Steps:**
1. Feature scaling with `scaler.pkl`
2. Missing value imputation (if needed)
3. Outlier handling

### Ultrasound Image Preprocessing

1. **Load Image**: Accept JPEG, PNG, GIF, BMP formats
2. **Convert**: RGB (grayscale → RGB if needed)
3. **Resize**: 224×224 pixels (CNN input size)
4. **Normalize**: Pixel values → [-1, 1]
5. **Batch**: Add batch dimension for inference

---

## 🧠 Machine Learning Models

### 1. Ensemble Classifier (`pcos_ensemble_model.pkl`)
- **Type**: Scikit-learn ensemble model
- **Input**: 14 symptom features (scaled)
- **Output**: Binary classification + probability
- **Accuracy**: Trained on PCOS dataset

### 2. CNN Model (`model.h5`)
- **Type**: TensorFlow/Keras convolutional neural network
- **Input**: 224×224×3 ultrasound images
- **Output**: Binary classification + probability
- **Architecture**: Standard CNN for medical image analysis

**Loading Models:**
```python
from ultrasound_predict import load_cnn_model, predict_ultrasound
import joblib

# Load ensemble model
ensemble_model = joblib.load("model/pcos_ensemble_model.pkl")

# Load CNN model
cnn_model = load_cnn_model()

# Get prediction
result = predict_ultrasound("path/to/ultrasound.jpg")
```

---

## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate

# Test symptom prediction endpoint
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

### Frontend Testing

```bash
cd frontend

# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)
- **Django** 4.2+ – Web framework
- **djangorestframework** – REST API toolkit
- **tensorflow** – Deep learning framework for CNN
- **scikit-learn** – Machine learning library
- **numpy** – Numerical computing
- **pandas** – Data manipulation
- **Pillow** – Image processing
- **joblib** – Model serialization

### Frontend (`package.json`)
- **React** 19+ – UI library
- **axios** – HTTP client
- **Vite** – Build tool

---

## 🔒 Security Considerations

✅ **File Upload Security**
- MIME type validation
- File size limits (10MB max)
- Temporary file cleanup
- Safe filename handling

✅ **API Security**
- CSRF protection enabled
- Input validation on all endpoints
- Error messages don't leak sensitive info
- Proper HTTP status codes

✅ **Data Privacy**
- No sensitive data stored long-term
- Uploaded images deleted after processing
- HIPAA compliance considerations (future)

---

## 🚨 Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Module not found: tensorflow` | TensorFlow not installed | Run `pip install -r requirements.txt` |
| `Model not found at path/model.h5` | Missing model file | Verify `model/model.h5` exists |
| `CORS error` | Frontend/backend mismatch | Check CORS settings in settings.py |
| `Image upload failed` | File too large or wrong format | Use JPEG/PNG, max 10MB |
| `Port 8000 already in use` | Django port conflict | Use `python manage.py runserver 8001` |

---

## 📝 Logging

Backend logs are printed to console during development:

```
INFO: CNN model loaded successfully
INFO: Image preprocessed successfully: shape=(1, 224, 224, 3)
INFO: PCOS prediction: PCOS Likely, confidence: 87.50%
INFO: Combined prediction: High Risk (72.00%)
```

For production, configure file logging in Django settings.

---

## 🔄 Workflow Diagram

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Stage 1: Symptom Questionnaire     │
│  (14 health-related questions)      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Ensemble Model Prediction          │
│  (Symptom Risk: 0-100%)             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Display Symptom Result             │
│  Option: Upload Ultrasound          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Stage 2: Ultrasound Upload         │
│  (Drag & drop or file select)       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  CNN Model Prediction               │
│  (Ultrasound Risk: 0-100%)          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Combine Predictions                │
│  Final = 0.6×Symptom + 0.4×Image    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Final Diagnosis                    │
│  • Combined Risk Score              │
│  • Risk Level (Low/Moderate/High)   │
│  • Clinical Recommendations         │
└─────────────────────────────────────┘
```

---

## 📚 Documentation Files

- **[WALKTHROUGH.md](./WALKTHROUGH.md)** – Step-by-step setup and usage guide
- **[API_REFERENCE.md](./API_REFERENCE.md)** – Detailed API documentation (optional)
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** – Development setup and contribution guidelines (optional)

---

## 🤝 Contributing

(Future: Add contribution guidelines)

---

## 📄 License

(Future: Add license information)

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: HerCare is a screening tool for informational purposes only and should **NOT** be considered a medical diagnosis. 

- Results are AI-powered predictions, not clinical diagnoses
- Always consult qualified healthcare professionals for proper evaluation
- This tool supplements, not replaces, professional medical consultation
- Users assume full responsibility for decisions based on results

---

## 📞 Support

For issues or questions:
1. Check [WALKTHROUGH.md](./WALKTHROUGH.md) for common problems
2. Review error messages in terminal/console
3. Verify all dependencies are installed correctly

---

## 🎉 What's Next?

- ✅ Two-stage PCOS prediction implemented
- 🔄 Model retraining pipeline (future)
- 📊 Results analytics dashboard (future)
- 🔐 User authentication & history (future)
- 🌍 Multi-language support (future)
- ☁️ Cloud deployment (AWS/Azure) (future)

---

**Built with ❤️ for women's health**
