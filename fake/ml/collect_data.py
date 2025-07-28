import tweepy
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

def get_user_data(username):
    try:
        user = client.get_user(username=username, user_fields=["created_at", "description", "profile_image_url", "public_metrics", "verified"])
        u = user.data
        metrics = u.public_metrics
        now = datetime.utcnow()
        account_age_days = (now - u.created_at).days

        return {
            "followers": metrics["followers_count"],
            "following": metrics["following_count"],
            "tweets": metrics["tweet_count"],
            "listed": metrics["listed_count"],
            "verified": int(u.verified),
            "bio_length": len(u.description or ""),
            "has_profile_pic": 0 if "default_profile_images" in (u.profile_image_url or "") else 1,
            "account_age_days": account_age_days,
            "follower_following_ratio": round(metrics["followers_count"] / (metrics["following_count"] + 1), 2)
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

usernames = ["@elonmusk", "@BillGates", "@some_random_fake", "@randomuser123"]

data = []
for user in usernames:
    print(f"Fetching {user}")
    user_data = get_user_data(user)
    if user_data:
        user_data["is_fake"] = 0 if "elon" in user or "gates" in user else 1
        data.append(user_data)

df = pd.DataFrame(data)
df.to_csv("data/twitter_users.csv", index=False)
print("Data saved to data/twitter_users.csv")