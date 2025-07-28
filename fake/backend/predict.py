from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load("fake_account_model.pkl")  # Make sure this model was trained using the full feature set

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        # Extract features in the same order as used during model training
        features = [
            data["followers"],
            data["following"],
            data["tweets"],
            data["listed"],
            data["verified"],
            data["bio_length"],
            data["has_profile_pic"],
            data["account_age_days"],
            data["follower_following_ratio"],
            data["avg_likes"],
            data["avg_retweets"],
            data["tweet_frequency"]
        ]

        # Convert to 2D array for prediction
        features_array = np.array([features])

        # Make prediction
        prediction = model.predict(features_array)[0]
        confidence = model.predict_proba(features_array)[0][prediction]

        return jsonify({
            "prediction": int(prediction),
            "result": "fake" if prediction == 1 else "real",
            "confidence": round(float(confidence) * 100, 2)
        })

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
