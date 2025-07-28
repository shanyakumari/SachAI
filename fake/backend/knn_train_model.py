import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the labeled dataset
df = pd.read_csv('fake_accounts.csv')

# Features to use
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

# Separate features and target
X = df[features]
y = df['label']

# Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train KNN model
knn_model = KNeighborsClassifier(n_neighbors=5)  # You can tune this value
knn_model.fit(X_train, y_train)

# Predict and evaluate
y_pred = knn_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ KNN Model accuracy: {accuracy:.2f}")
print("📋 Classification report:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(knn_model, 'knn_fake_account_model.pkl')
print("✅ KNN model saved as knn_fake_account_model.pkl")
