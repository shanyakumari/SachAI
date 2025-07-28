import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump

X = pd.read_csv("data/features.csv")
y = pd.read_csv("data/labels.csv")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train.values.ravel())

dump(model, "backend/model.pkl")
print("Model trained and saved to backend/model.pkl")