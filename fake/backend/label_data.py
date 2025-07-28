import pandas as pd

# Load the updated dataset with additional features
df = pd.read_csv("fake_accounts.csv")

# Labeling logic using basic + tweet activity features
def label_account(row):
    # Clearly real accounts
    if row['verified'] == 1 or row['followers'] > 5000 or row['avg_likes'] > 100 or row['avg_retweets'] > 50:
        return 0  # Real

    # Reasonably real accounts (human-like activity)
    if (
        row['followers'] > 100 and 
        row['tweets'] > 20 and 
        row['has_profile_pic'] == 1 and
        row['avg_likes'] > 5 and 
        row['tweet_frequency'] > 0.2
    ):
        return 0  # Real

    # Clearly fake accounts (low metrics)
    if (
        row['followers'] < 10 and 
        row['tweets'] < 5 and 
        row['has_profile_pic'] == 0
    ) or (
        row['followers'] < 10 and 
        row['listed'] < 1 and 
        row['avg_likes'] == 0 and 
        row['tweet_frequency'] == 0
    ):
        return 1  # Fake

    # Not enough signal — uncertain
    return -1

# Apply labeling
df['label'] = df.apply(label_account, axis=1)

# Drop uncertain
df = df[df['label'] != -1]

# Save to CSV
df.to_csv("labeled_fake_accounts.csv", index=False)
print("✅ Labeled data saved to labeled_fake_accounts.csv")
print("📊 Label distribution:\n", df['label'].value_counts())
