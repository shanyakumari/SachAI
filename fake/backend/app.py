from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime, timezone
import requests
from dateutil import parser
from sklearn.preprocessing import StandardScaler

# ✅ Twitter Bearer Token
BEARER_TOKEN = process.env.BEARER_TOKEN

# ✅ Load models
rf_model = joblib.load("fake_account_model.pkl")
knn_model = joblib.load("knn_fake_account_model.pkl")
svc_model = joblib.load("linear_svc_fake_account_model.pkl")
svc_scaler = joblib.load("linear_svc_scaler.pkl")  # Scaler for SVC

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Fake Account Detection API with RF, KNN, and SVC is running!"

@app.route('/predict-twitter', methods=['POST'])
def predict_twitter():
    try:
        data = request.get_json()
        username = data.get('username')
        model_type = data.get('model', 'random_forest').lower()

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # ✅ Fetch Twitter user data
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        params = {
            "user.fields": "created_at,description,verified,profile_image_url,public_metrics"
        }
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return jsonify({'error': 'Twitter API error', 'details': response.text}), 500

        user = response.json().get("data")
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # ✅ Extract features
        metrics = user["public_metrics"]
        followers = metrics.get("followers_count", 0)
        following = metrics.get("following_count", 0)
        tweets = metrics.get("tweet_count", 0)
        listed = metrics.get("listed_count", 0)
        verified = int(user.get("verified", False))
        bio = user.get("description", "")
        bio_length = len(bio)
        has_profile_pic = int(user.get("profile_image_url") is not None)

        created_at = parser.isoparse(user["created_at"])
        account_age_days = (datetime.now(timezone.utc) - created_at).days
        ratio = followers / following if following else 0

        features = np.array([[followers, following, tweets, listed, verified,
                              bio_length, has_profile_pic, account_age_days, ratio]])

        # ✅ Model selection
        if model_type == 'random_forest':
            model = rf_model
            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0][1] * 100
        elif model_type == 'knn':
            model = knn_model
            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0][1] * 100
        elif model_type == 'linear_svc':
            scaled_features = svc_scaler.transform(features)
            model = svc_model
            prediction = model.predict(scaled_features)[0]
            proba = 100.0  # SVC doesn't support predict_proba by default
        else:
            return jsonify({'error': 'Invalid model. Choose rf, knn, or svc'}), 400

        return jsonify({
            "is_fake": bool(prediction),
            "confidence": round(proba, 2),
            "model_used": model_type,
            "username": user.get("username"),
            "name": user.get("name"),
            "bio": bio,
            "profile_image_url": user.get("profile_image_url"),
            "followers": followers,
            "following": following,
            "tweets": tweets,
            "created_at": created_at.strftime("%Y-%m-%d"),
            "account_age_days": account_age_days
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
