# HerCare Setup & Usage Walkthrough

## 📖 Complete Guide to Getting Started with HerCare

This guide walks you through:
1. Initial setup (backend & frontend)
2. User registration and authentication
3. Running the application
4. Testing all features (authentication + PCOS screening)
5. Troubleshooting common issues

**What's New in This Version:**
- 🔐 **User Authentication System** - Secure login/registration with JWT tokens
- ⚛️ **React Frontend** - Modern single-page application with routing
- 🎨 **Healthcare UI Theme** - Soft pastel colors and responsive design
- 🛡️ **Protected Routes** - All PCOS features require user authentication

---

## Part 1: Initial Setup (One-time)

### Step 1.1: Verify Prerequisites

Before starting, ensure you have:

```bash
# Check Python version (3.11+)
python --version
# Output: Python 3.11.x or higher

# Check Node.js version (18+)
node --version
# Output: v18.x or higher

# Check npm version
npm --version
# Output: v9.x or higher
```

**Don't have these?**
- Python: Download from https://www.python.org/downloads/
- Node.js: Download from https://nodejs.org/

### Step 1.2: Clone/Navigate to Project

```bash
# Navigate to HerCare directory
cd /path/to/HerCare
pwd  # Verify you're in the right location
```

---

## Part 2: Backend Setup

### Step 2.1: Create Python Virtual Environment

```bash
cd backend
python -m venv venv
```

This creates a `venv/` folder with isolated Python packages.

### Step 2.2: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

✅ **You'll see `(venv)` prefix in terminal when activated**

### Step 2.3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django & REST framework
- TensorFlow (for CNN model)
- Scikit-learn (for ensemble model)
- Pillow (for image processing)
- Other required packages

⏳ **This may take 3-5 minutes on first install (TensorFlow is large)**

### Step 2.4: Verify Installation

```bash
python -c "import tensorflow; print('TensorFlow version:', tensorflow.__version__)"
python -c "import sklearn; print('Scikit-learn installed')"
python -c "import django; print('Django version:', django.__version__)"
```

✅ All should print without errors

### Step 2.5: Start Django Server

```bash
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 05, 2026 - 10:30:45
Django version 4.2.11, using settings 'hercare_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

✅ **Backend is now running on http://127.0.0.1:8000**

---

## Part 3: Frontend Setup

### Step 3.1: Open New Terminal

Keep the Django server running in the first terminal, open a **new terminal** window.

### Step 3.2: Navigate to Frontend

```bash
cd /path/to/HerCare/frontend
```

### Step 3.3: Install Node Dependencies

```bash
npm install
```

This reads `package.json` and installs:
- React 19
- Vite (bundler)
- Axios (HTTP client)
- Other dependencies

⏳ **Takes 1-2 minutes**

### Step 3.4: Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v7.2.4  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

✅ **Frontend is now running on http://localhost:5173**

---

## Part 4: Access the Application

### Step 4.1: Open Browser

Visit: **http://localhost:5173**

You should see:
- HerCare landing page with navigation
- "Welcome to HerCare" header
- Login/Register buttons in navbar

### Step 4.2: Verify Backend Connection

The frontend automatically makes API calls to the backend. If you see:
- ✅ Page loads with navbar → Backend is reachable
- ❌ "Failed to connect to backend" → See Troubleshooting section

---

## Part 5: User Authentication Setup

### Step 5.1: Register New Account

**Step 1:** Click "Register" in the navbar

**Step 2:** Fill registration form:
```
First Name: Jane
Last Name: Doe
Email: jane.doe@example.com
Password: securepassword123
Confirm Password: securepassword123
```

**Step 3:** Click "Create Account"

**Expected Result:**
- Success message: "Account created successfully!"
- Redirected to login page

### Step 5.2: Login to Account

**Step 1:** Use the account you just created:
```
Email: jane.doe@example.com
Password: securepassword123
```

**Step 2:** Click "Login"

**Expected Result:**
- Success message: "Login successful!"
- Redirected to dashboard
- Navbar shows "Dashboard" and "Logout" options

### Step 5.3: Verify Authentication

**Check 1:** Navbar should show user greeting
**Check 2:** Can access Dashboard and PCOS Detector
**Check 3:** JWT tokens stored in browser (check DevTools → Application → Local Storage)

---

## Part 6: Complete Workflow Test

### Test Case 1: User Dashboard

**Step 1:** After login, you're on the Dashboard

**Expected Result:**
- Welcome message with user name
- "Start PCOS Screening" button
- Last screening result (if any)

### Test Case 2: Symptom Prediction Only

**Step 1:** Click "Start PCOS Screening" or navigate to PCOS Detector

**Step 2:** Fill the symptom form
```
Basic Information:
- Age: 25 years
- Weight: 65 kg
- Height: 160 cm

Menstrual & Pregnancy:
- Irregular Cycle? YES
- Cycle Length: 45 days
- Ever Pregnant? NO
- Abortions: 0

Physical Symptoms:
- Weight Gain? YES
- Hair Growth? YES
- Skin Darkening? YES
- Hair Loss? NO
- Acne? YES

Lifestyle:
- Fast Food? YES
- Regular Exercise? NO
```

**Step 3:** Click "Get Symptom-Based Assessment"

**Expected Result:**
- Screen shows: "PCOS Risk from Symptoms: 62%"
- Button appears: "Next: Upload Ultrasound"
- Can click "Start Over" to reset

### Test Case 3: Ultrasound Upload

**Step 1:** Click "Next: Upload Ultrasound"

**Step 2:** Upload an ultrasound image
- Click "Upload Ultrasound Image" or drag-and-drop
- Select a valid image file (JPEG, PNG, GIF, BMP)
- Max size: 10MB

**Step 3:** See preview of uploaded image

**Step 4:** Click "Analyze Image"

**Expected Result:**
```
Stage 1: Symptom Analysis → 62%
Stage 2: Ultrasound Analysis → 87%

Final PCOS Risk Assessment → 72% → High Risk
```

### Test Case 4: View Results in Dashboard

**Step 1:** After completing screening, return to Dashboard

**Expected Result:**
- Latest screening result displayed
- Date and risk level shown
- Can start new screening

### Test Case 5: Logout and Login Again

**Step 1:** Click "Logout" in navbar

**Step 2:** Login again with same credentials

**Expected Result:**
- Previous screening results still available
- Seamless authentication flow

---

## Part 6: Understanding the Results

### Symptom Stage Output
```json
{
  "prediction": 1,           // 1 = PCOS detected, 0 = Not detected
  "pcos_probability": 62.50, // Risk percentage (0-100)
  "result": "PCOS Likely"
}
```

### Ultrasound Stage Output
```json
{
  "success": true,
  "prediction": "PCOS Likely",
  "confidence": 87.50,       // CNN confidence (0-100)
  "probability": 0.875       // CNN confidence (0-1)
}
```

### Final Combined Output
```json
{
  "final_probability": 0.72,  // 72% = 0.6×0.625 + 0.4×0.875
  "final_confidence": 72.00,
  "risk_level": "High Risk",  // High ≥70%, Moderate 40-70%, Low <40%
  "components": {
    "symptom_probability": 0.625,
    "ultrasound_probability": 0.875,
    "symptom_weight": 0.6,
    "ultrasound_weight": 0.4
  }
}
```

---

## Part 7: API Testing (Advanced)

If you want to test the APIs directly:

### Test Authentication APIs

#### Register New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "password": "securepassword123"
  }'
```

#### Login User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.doe@example.com",
    "password": "securepassword123"
  }'
```

**Save the access token from login response for authenticated requests**

#### Get User Profile (Authenticated)
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

#### Get User Dashboard (Authenticated)
```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Test PCOS APIs (Authenticated)

#### Test Symptom API
```bash
curl -X POST http://127.0.0.1:8000/api/pcos/form-predict/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
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

#### Test Ultrasound API
```bash
curl -X POST http://127.0.0.1:8000/api/ultrasound/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -F "ultrasound_image=@/path/to/ultrasound.jpg"
```

#### Test Combined Prediction API
```bash
curl -X POST http://127.0.0.1:8000/api/combined-prediction/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -d '{
    "symptom_probability": 0.625,
    "ultrasound_probability": 0.875,
    "symptom_weight": 0.6,
    "ultrasound_weight": 0.4
  }'
```

---

## Part 8: Troubleshooting

### ❌ Problem: "Failed to connect to backend"

**Cause:** Django server not running or CORS issue

**Solution:**
```bash
# Terminal 1 - Check Django is running
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Check frontend is running
cd frontend
npm run dev

# Wait 10 seconds for both to fully start
# Refresh browser at http://localhost:5173
```

---

### ❌ Problem: "Module not found: tensorflow"

**Cause:** Dependencies not installed

**Solution:**
```bash
cd backend
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### ❌ Problem: Port 8000 Already in Use

**Cause:** Another application using port 8000

**Solution:**
```bash
# Use a different port
python manage.py runserver 8001

# Then in frontend API calls, update to http://127.0.0.1:8001
```

---

### ❌ Problem: "cannot open shared object file: tensorflow"

**Cause:** TensorFlow dependencies missing (Linux)

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# Then reinstall
pip install --upgrade tensorflow
```

---

### ❌ Problem: Port 5173 Already in Use

**Cause:** Another Vite server running

**Solution:**
```bash
# Auto-select different port
npm run dev -- --port 5174
```

---

### ❌ Problem: "Authentication failed" or "Token expired"

**Cause:** JWT token expired or invalid

**Solution:**
1. Logout and login again
2. Check browser time is correct
3. Clear browser localStorage if needed

---

### ❌ Problem: "CORS error" in browser console

**Cause:** Frontend trying to access backend with wrong URL

**Solution:**
1. Ensure backend runs on http://127.0.0.1:8000
2. Ensure frontend runs on http://localhost:5173
3. Check CORS settings in Django settings.py

---

### ❌ Problem: Registration fails with "Email already exists"

**Cause:** User already registered

**Solution:**
1. Use different email address
2. Or login with existing account
3. Check database: `python manage.py shell` then `from accounts.models import CustomUser; CustomUser.objects.all()`

---

### ❌ Problem: Login fails with "Invalid credentials"

**Cause:** Wrong email/password or account doesn't exist

**Solution:**
1. Verify email and password are correct
2. Check if account exists in database
3. Reset password by deleting and recreating account

---

### ❌ Problem: "Network Error" on API calls

**Cause:** Backend server not running or wrong URL

**Solution:**
1. Verify Django server is running on port 8000
2. Check API base URL in frontend/src/services/api.js
3. Test backend directly: curl http://127.0.0.1:8000/api/auth/profile/

---

### ❌ Problem: Image Upload Fails

**Cause:** File too large, wrong format, or temporary directory issue

**Solution:**
1. Use JPEG, PNG, GIF, or BMP format
2. Keep file under 10MB
3. Check write permissions in /tmp (macOS/Linux) or %TEMP% (Windows)

---

### ❌ Problem: CNN Model Not Found

**Cause:** Missing `model/model.h5` file

**Solution:**
Verify file exists:
```bash
ls backend/pcos_screener/model/
# Should show: model.h5, pcos_ensemble_model.pkl, scaler.pkl
```

---

### ❌ Problem: Ensemble Model Not Found

**Cause:** Missing `pcos_ensemble_model.pkl` or `scaler.pkl`

**Solution:**
```bash
ls backend/pcos_screener/model/pcos_ensemble_model.pkl
ls backend/pcos_screener/model/scaler.pkl
# Both files must exist
```

---

### ❌ Problem: Slow Model Loading

**Cause:** First prediction loads model from disk (expected)

**Solution:**
- First prediction: 5-10 seconds (model loading)
- Subsequent: <1 second (cached)
- This is normal behavior

---

## Part 9: Stopping the Servers

### Stop Backend
In the Django terminal, press:
```
CTRL + C
```

Then deactivate virtual environment:
```bash
deactivate
```

### Stop Frontend
In the Vite terminal, press:
```
CTRL + C
```

---

## Part 10: Running Again Later

Next time you want to run HerCare:

**Terminal 1 - Backend:**
```bash
cd /path/to/HerCare/backend
source venv/bin/activate        # macOS/Linux
# or venv\Scripts\activate       # Windows
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd /path/to/HerCare/frontend
npm run dev
```

**Browser:**
```
http://localhost:5173
```

---

## Part 11: Production Deployment

### Build Frontend for Production
```bash
cd frontend
npm run build
# Creates optimized files in dist/
```

### Deploy Backend
```bash
cd backend
gunicorn hercare_project.wsgi

# Or use Docker/Kubernetes for scaling
```

See deployment documentation for cloud providers (AWS, Azure, Google Cloud).

---

## Part 12: File Organization

Understand the project structure:

```
HerCare/
├── README.md                    ← Project overview
├── WALKTHROUGH.md               ← This file
├── backend/
│   ├── requirements.txt         ← Python dependencies
│   ├── pcos_screener/
│   │   ├── ultrasound_predict.py    ← CNN inference code
│   │   ├── api_views.py             ← API endpoints
│   │   ├── api_urls.py              ← API routes
│   │   └── model/
│   │       ├── model.h5             ← CNN model
│   │       ├── pcos_ensemble_model.pkl ← Symptom model
│   │       └── scaler.pkl           ← Feature scaler
│   └── venv/                    ← (Don't edit) Python packages
│
└── frontend/
    ├── package.json             ← Node dependencies
    ├── src/
    │   ├── App.jsx              ← Main application
    │   ├── App.css              ← Main styles
    │   └── components/
    │       ├── UltrasoundUpload.jsx    ← Image upload
    │       └── UltrasoundUpload.css
    └── node_modules/            ← (Don't edit) Node packages
```

---

## Part 13: Next Steps

### For Users:
- ✅ Use the application for PCOS screening
- ⚠️ Remember: This is screening only, not diagnosis
- 📋 Consult qualified healthcare professionals for proper evaluation

### For Developers:
- 🔧 Modify symptom questions in `App.jsx`
- 🧠 Replace models in `backend/pcos_screener/model/`
- 🎨 Customize UI in `App.css` and component style files
- 🔌 Add more API endpoints in `api_views.py`

---

## Part 14: Key Files Reference

| File | Purpose | Modify For |
|------|---------|-----------|
| `ultrasound_predict.py` | CNN inference | Changing image size, normalization |
| `api_views.py` | API logic | Adding endpoints, changing validation |
| `App.jsx` | Main workflow | Changing questions, flow, UI text |
| `UltrasoundUpload.jsx` | Image upload | File validation, upload limits |
| `requirements.txt` | Dependencies | Updating packages, adding features |
| `package.json` | Frontend deps | Adding libraries, new features |

---

## Part 15: Performance Tips

- 💾 **Cache model loading** – First prediction slower due to model loading
- 📊 **Optimize images** – Smaller images = faster upload
- 🗜️ **Compress models** – Reduce model.h5 size for faster loading
- 🔄 **Use batch predictions** – Process multiple images together (future feature)

---

## ✅ Checklist - You're Ready When:

- [x] Python 3.11+ installed
- [x] Node.js 18+ installed
- [x] Backend virtual environment created
- [x] Requirements installed (`pip install -r requirements.txt`)
- [x] Django server running on port 8000
- [x] Frontend server running on port 5173
- [x] Application loads at http://localhost:5173
- [x] Can submit symptom form
- [x] Can upload ultrasound image
- [x] Can view final combined prediction

---

## 🎉 You Did It!

HerCare is now fully operational. Start screening for PCOS!

For detailed information, see:
- **README.md** – Project overview
- **API endpoints** – Detailed in README.md

---

**Happy screening! Built with ❤️ for women's health**
