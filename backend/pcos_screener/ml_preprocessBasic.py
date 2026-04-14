import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# Load the cleaned dataset
df = pd.read_csv("pcos_screener/data/pcos_clean_v1.csv")

# Standardize column names
df.columns = (
    df.columns
    .str.strip()  # remove leading/trailing spaces
    .str.replace(' ', '_')  # replace spaces with underscores
    .str.replace(r'[^\w]', '', regex=True)  # remove special characters
    .str.lower()  # convert to lowercase
)

# Define basic features (excluding BMI)
basic_features = [
    'age_yrs', 'weight_kg', 'heightcm', 'cycleri', 'cycle_lengthdays',
    'pregnantyn', 'no_of_abortions', 'weight_gainyn', 'hair_growthyn',
    'skin_darkening_yn', 'hair_lossyn', 'pimplesyn', 'fast_food_yn', 'regexerciseyn'
]

# Target variable
target = 'pcos_yn'

# Select the basic features and target
df_basic = df[basic_features + [target]]

# Handle missing values
df_basic = df_basic.dropna()

# Split into train and test sets
X = df_basic[basic_features]
y = df_basic[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define individual models
model_rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)

model_lr = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    random_state=42
)

model_gb = GradientBoostingClassifier(
    n_estimators=150,
    random_state=42
)

# Create Voting Ensemble
ensemble_model = VotingClassifier(
    estimators=[('rf', model_rf), ('lr', model_lr), ('gb', model_gb)],
    voting='soft'  # uses predicted probabilities
)

# Train the ensemble
ensemble_model.fit(X_train_scaled, y_train)

# Predictions and evaluation
y_pred = ensemble_model.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Optional: save model and scaler
import joblib
joblib.dump(ensemble_model, "pcos_screener/model/pcos_ensemble_model.pkl")
joblib.dump(scaler, "pcos_screener/model/scaler.pkl")
joblib.dump(basic_features, "pcos_screener/model/features.pkl")
