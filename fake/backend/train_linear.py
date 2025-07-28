import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Load the labeled dataset
df = pd.read_csv('fake_accounts.csv')

# Feature list
features = [
    'followers',
    'following',
    'tweets',
    'listed',
    'verified',
    'bio_length',
    'has_profile_pic',
    'account_age_days',
    'follower_following_ratio'
]

# Separate features and label
X = df[features]
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train LinearSVC model
svc_model = LinearSVC(max_iter=10000, random_state=42)
svc_model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = svc_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Linear SVC Model accuracy: {accuracy:.2f}")
print("📋 Classification report:\n", classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(svc_model, 'linear_svc_fake_account_model.pkl')
joblib.dump(scaler, 'linear_svc_scaler.pkl')
print("✅ LinearSVC model saved as linear_svc_fake_account_model.pkl")
print("✅ Scaler saved as linear_svc_scaler.pkl")
