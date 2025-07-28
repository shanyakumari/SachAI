import requests
import pandas as pd
from datetime import datetime
import time

# ✅ Your Twitter Bearer Token
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAF1s0gEAAAAAxbp7XznpeR79vIVcAHXYBUSGlG0%3D8qYZ385ai1j6VE1v2bjPRPjIUixqylDfdRZhz9kjGeVWfMDpV6"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# ✅ Twitter usernames to test
usernames = [
    "nasa", "bhoomeme", "elonmusk", "BarackObama", "cnnbrk", "justinbieber", "imVkohli",
    "katyperry", "KimKardashian", "realDonaldTrump", "umarants", "ItsAmitTrivedi", "TheCinesthetic",
    "StackOverflow", "bbcnews", "nytimes", "WHO", "UN", "xyz284284", "dmforfeet2", "Sammysupersa",
    "ndiessjd", "Nyapt1", "shanyayaar", "RAITtheWall", "wall_rait", "xyz284284", "evvss",
    "saeegivingup", "ichigoxt"
]

# Twitter API endpoint for user info
url = "https://api.twitter.com/2/users/by"

params = {
    "usernames": ",".join(usernames),
    "user.fields": "created_at,description,verified,profile_image_url,public_metrics"
}

# Send request to get user data
response = requests.get(url, headers=headers, params=params)
print("🌐 API status:", response.status_code)

if response.status_code != 200:
    print("❌ Error response from Twitter API:", response.text)
    exit()

data = response.json()
rows = []

# Function to get recent tweets of a user
def get_recent_tweets(user_id, max_results=10):
    tweet_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    tweet_params = {
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics"
    }
    tweet_response = requests.get(tweet_url, headers=headers, params=tweet_params)
    if tweet_response.status_code != 200:
        print(f"⚠️ Could not fetch tweets for user {user_id}")
        return []
    return tweet_response.json().get("data", [])

# Process each user
for user in data.get("data", []):
    print("✅ Extracting data for:", user.get("username", "N/A"))
    metrics = user.get("public_metrics", {})
    user_id = user.get("id")

    followers = metrics.get("followers_count", 0)
    following = metrics.get("following_count", 0)
    tweet_count = metrics.get("tweet_count", 0)
    listed = metrics.get("listed_count", 0)
    verified = int(user.get("verified", False))
    bio_length = len(user.get("description", "") or "")
    has_profile_pic = int(user.get("profile_image_url") is not None)

    created_at_str = user.get("created_at")
    if created_at_str:
        created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        account_age_days = (datetime.utcnow() - created_at).days
    else:
        account_age_days = 0

    ratio = followers / following if following else 0

    # ➕ Get recent tweet activity
    tweets_data = get_recent_tweets(user_id, max_results=20)
    total_likes = 0
    total_retweets = 0
    tweet_times = []

    for tweet in tweets_data:
        pub_metrics = tweet.get("public_metrics", {})
        total_likes += pub_metrics.get("like_count", 0)
        total_retweets += pub_metrics.get("retweet_count", 0)
        created_time = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        tweet_times.append(created_time)

    avg_likes = total_likes / len(tweets_data) if tweets_data else 0
    avg_retweets = total_retweets / len(tweets_data) if tweets_data else 0

    tweet_frequency = 0
    if len(tweet_times) > 1:
        days_range = (max(tweet_times) - min(tweet_times)).days or 1
        tweet_frequency = len(tweet_times) / days_range

    # Basic fake label rule
    label = 1 if followers < 10 and tweet_count < 10 and not verified else 0

    # Append data
    rows.append({
        "followers": followers,
        "following": following,
        "tweets": tweet_count,
        "listed": listed,
        "verified": verified,
        "bio_length": bio_length,
        "has_profile_pic": has_profile_pic,
        "account_age_days": account_age_days,
        "follower_following_ratio": ratio,
        "avg_likes": avg_likes,
        "avg_retweets": avg_retweets,
        "tweet_frequency": tweet_frequency,
        "label": label
    })

    time.sleep(1)  # prevent rate limiting

# ✅ Save to CSV
df = pd.DataFrame(rows)
df.to_csv("fake_accounts.csv", index=False)
print("📁 Data saved to fake_accounts.csv")
