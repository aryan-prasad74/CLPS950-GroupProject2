import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from Jamin import profile_track_analysis as analyze_tracks

#clear cache
if os.path.exists(".cache"):
    os.remove(".cache")

print("Starting Spotify Mood Analysis Program")

#run profile track analysis
print("\nRunning Track Analysis ...")
analyzed_tracks, compound_scores, cumulative_moods = analyze_tracks()


##########################################################

## GENERATING PROFILE ANALYSIS DIAGRAMS ##

sns.set(style="whitegrid")
fig1, axs1 = plt.subplots(2, 1, figsize=(12, 8))

# 1A: Bar plot of sentiment scores per song
sns.barplot(
    x=compound_scores,
    y=analyzed_tracks,
    ax=axs1[0],
    palette="coolwarm",
    dodge=False,   # ensure no hue shifting
    hue=analyzed_tracks,
    legend=False
)
axs1[0].set_title("Sentiment Scores per Song")
axs1[0].set_xlabel("Compound Score")
axs1[0].set_ylabel("Track")

# 1B: Histogram of sentiment score distribution
sns.histplot(
    compound_scores,
    bins=20,
    kde=True,
    ax=axs1[1],
    color="skyblue"
)
axs1[1].set_title("Distribution of Sentiment Scores")
axs1[1].set_xlabel("Compound Score")
axs1[1].set_ylabel("Frequency")

fig1.tight_layout()


## Generating final summary diagrams ##

fig2, axs2 = plt.subplots(1, 2, figsize=(14, 6))

# 2A: Scatter & line of mood inputs by iteration
iterations = list(range(1, len(cumulative_moods) + 1))
axs2[0].scatter(iterations, cumulative_moods, s=60)
axs2[0].plot(iterations, cumulative_moods, linestyle="--", alpha=0.6)
axs2[0].axhline(0, color="gray", linewidth=1)
axs2[0].set_title("Mood Input Values by Iteration")
axs2[0].set_xlabel("Iteration Number")
axs2[0].set_ylabel("Mood Index (–1 to +1)")
axs2[0].set_xticks(iterations)
axs2[0].set_ylim(-1.05, 1.05)

# 2B: Pie chart of overall mood distribution
mood_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
for score in cumulative_moods:
    if score > 0.05:
        mood_counts["Positive"] += 1
    elif score < -0.05:
        mood_counts["Negative"] += 1
    else:
        mood_counts["Neutral"] += 1

labels = list(mood_counts.keys())
sizes  = list(mood_counts.values())
colors = ["#99ff99", "#ffcc99", "#ff9999"]

axs2[1].pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors
)
axs2[1].set_title("Overall Mood Distribution")
axs2[1].axis("equal")  # keep pie circular

fig2.tight_layout()


plt.show()

print("\nComplete! Thanks for using our program.")


