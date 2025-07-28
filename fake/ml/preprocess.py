import pandas as pd

df = pd.read_csv("data/twitter_users.csv")
X = df.drop("is_fake", axis=1)
y = df["is_fake"]
X.to_csv("data/features.csv", index=False)
y.to_csv("data/labels.csv", index=False)
print("Preprocessing done.")