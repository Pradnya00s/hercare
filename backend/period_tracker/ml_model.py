import numpy as np
from sklearn.linear_model import LogisticRegression

# 🔥 Dummy training data (you can explain this in viva)
# Features: [avg_cycle_length, variation, max_gap]
X = np.array([
    [28, 2, 30],
    [30, 3, 32],
    [27, 2, 29],
    [35, 10, 50],
    [40, 12, 60],
    [22, 8, 20],
])

# Labels: 0 = regular, 1 = irregular
y = np.array([0, 0, 0, 1, 1, 1])

# Train model once
model = LogisticRegression()
model.fit(X, y)


def predict_irregularity(avg, variation, max_gap):
    features = np.array([[avg, variation, max_gap]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "is_irregular": bool(prediction),
        "confidence": round(probability * 100, 2)
    }