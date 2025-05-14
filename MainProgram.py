import os

import matplotlib.pyplot as plt
import seaborn as sns

from Jamin import profile_track_analysis as analyze_tracks

#clear cache
if os.path.exists(".cache"):
    os.remove(".cache")

print("Starting Spotify Mood Analysis Program")

#run profile track analysis
print("\nRunning Track Analysis ...")
analyzed_tracks, compound_scores = analyze_tracks()

# generate diagrams
sns.set(style = "whitegrid") 
fig, axs = plt.subplots(2, 1, figsize = (12, 6))

#Bar Plot- visualizes sentiment scores per song
sns.barplot(x = compound_scores, y = analyzed_tracks, ax = axs[0], palette = "coolwarm")
axs[0].set_title("Sentiment Scores per Song")
axs[0].set_ylabel("Compound Score")
axs[0].set_xlabel("Tracks")

#Historgram - visualizes distribution of sentiment scores
sns.histplot(compound_scores, bins = 20, kde = True, ax = axs[1], color = 'skyblue')
axs[1].set_title("Distribution of Sentiment Scores")
axs[1].set_ylabel("Compound Score")
axs[1].set_xlabel("Frequency")

plt.tight_layout()
plt.show()

print("\nComplete! Thanks for using our program.")