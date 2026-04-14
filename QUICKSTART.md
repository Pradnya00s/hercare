# 🚀 HerCare – Quick Start Guide

## Get Started in 5 Minutes

### Prerequisites
- ✅ Python 3.11+ ([download](https://python.org/downloads/))
- ✅ Node.js 18+ ([download](https://nodejs.org/))
- ✅ Terminal/Command Prompt

---

## Step 1: Navigate to Project
```bash
cd /path/to/HerCare
```

---

## Step 2: Start Backend

**Terminal 1:**
```bash
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# OR
venv\Scripts\activate            # Windows

# Create .env file with API key
# Get GEMINI_API_KEY from https://ai.google.dev/
cat > .env << EOF
GEMINI_API_KEY=your_key_here
EOF

# Install dependencies
pip install -r requirements.txt

# Start server
python manage.py runserver
```

✅ Backend running: http://127.0.0.1:8000

---

## Step 3: Start Frontend

**Terminal 2 (New):**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend running: http://localhost:5173

---

## Step 4: Access Application

Visit: **http://localhost:5173**

---

## Step 5: Test Workflow

### Features to Test:

**1. PCOS Screening**
   - Login/Register
   - Fill symptom form  
   - Upload ultrasound image
   - See combined risk assessment

**2. Period Tracker**
   - Log menstrual cycles
   - Track daily symptoms
   - View ovulation predictions
   - Detect symptom patterns

**3. AI Health Companion**
   - Open AI Health page
   - Ask a health question
   - Get response from Google Gemini AI

---

## Quick Test Case:
1. Register: jane@test.com / Pass123!
2. Go to PCOS Detector → Fill form
3. Upload a test ultrasound image
4. View results
5. Try Period Tracker & AI Health pages

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](./README.md) | Project overview & features |
| [WALKTHROUGH.md](./WALKTHROUGH.md) | Step-by-step setup & troubleshooting |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | Development, extending features |
| [API_REFERENCE.md](./API_REFERENCE.md) | Complete API documentation |

---

## 🆘 Troubleshooting

### Backend won't start?
```bash
# Make sure you're in backend folder with venv activated
cd backend
source venv/bin/activate  # macOS/Linux
python manage.py runserver
```

### Frontend won't start?
```bash
# Make sure Node.js is installed
node --version  # Should be v18+
npm --version   # Should be v9+

cd frontend
npm install  # Reinstall if needed
npm run dev
```

### Port already in use?
```bash
# Use different port
python manage.py runserver 8001  # Backend on 8001
npm run dev -- --port 5174       # Frontend on 5174
```

### "Cannot find module"?
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## 🎯 What You Can Do

✅ **Symptom-based PCOS screening** (14 health questions)
✅ **Ultrasound image analysis** (upload scan for CNN prediction)
✅ **Combined diagnosis** (weighted prediction from both)
✅ **Risk stratification** (Low/Moderate/High risk assessment)

---

## 📊 Architecture

```
Browser (React)
    ↓↑
http://localhost:5173
    ↓↑
Vite Dev Server
    ↓↑
API Calls (Axios)
    ↓↑
http://127.0.0.1:8000
    ↓↑
Django REST API
    ↓
├── Symptom Prediction (Ensemble Model)
├── Ultrasound Analysis (CNN Model)
└── Combined Prediction (Weighted Average)
```

---

## 📁 Key Files

| File | What It Does |
|------|--------------|
| `backend/pcos_screener/ultrasound_predict.py` | CNN image analysis |
| `backend/pcos_screener/api_views.py` | API endpoints |
| `frontend/src/App.jsx` | Main workflow |
| `frontend/src/components/UltrasoundUpload.jsx` | Image upload UI |

---

## 💡 Tips

1. **First ultrasound prediction slow?** → Model loading on first use (normal)
2. **Want to train your own model?** → See DEVELOPMENT.md
3. **Need to add more questions?** → See DEVELOPMENT.md
4. **Want to deploy?** → See DEVELOPMENT.md Deployment section

---

## ⌚ Typical Duration

- Setup: **5-10 minutes**
- First test run: **1-2 minutes**
- Each prediction: **<1 second** (after initial load)

---

## 🎓 Learning Path

1. **Beginner**: Use the app, understand the workflow
2. **Intermediate**: Read DEVELOPMENT.md, modify UI
3. **Advanced**: Add new endpoints, retrain models

---

## 🔐 Security Notes

- Don't share your Django `SECRET_KEY`
- For production, set `DEBUG=False`
- Use HTTPS in production
- Keep dependencies updated: `pip list --outdated`

---

## 📞 Need Help?

1. Check [WALKTHROUGH.md](./WALKTHROUGH.md) for detailed setup
2. See [DEVELOPMENT.md](./DEVELOPMENT.md) for advanced topics
3. Check terminal for error messages
4. See [API_REFERENCE.md](./API_REFERENCE.md) for API details

---

## 🎉 You're All Set!

**HerCare is now running. Start screening!**

---

**Questions? See WALKTHROUGH.md for complete guide.**
