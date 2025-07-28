import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the updated labeled dataset
df = pd.read_csv('labeled_fake_accounts.csv')

# Updated feature list
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

# Features and target
X = df[features]
y = df['label']

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model accuracy: {accuracy:.2f}")
print("📋 Classification report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'fake_account_model.pkl')
print("✅ Model saved as fake_account_model.pkl")
