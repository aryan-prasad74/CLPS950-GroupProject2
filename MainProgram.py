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

## Generating final summary diagrams ##

#Mood over time
sns.set(style="whitegrid")
fig, axs = plt.subplots(1, 2, figsize = (12, 6))
iterations = list(range(1, len(cumulative_moods) + 1))
    
plt.figure(figsize=(10, 5))
plt.scatter(iterations, cumulative_moods, s=60)
plt.plot(iterations, cumulative_moods, linestyle='--', alpha=0.6)
plt.axhline(0, color='gray', linewidth=1)
    
plt.title("Mood Input Values by Iteration")
plt.xlabel("Iteration Number")
plt.ylabel("Mood Index (-1 to +1)")
plt.xticks(iterations)
plt.ylim(-1.05, 1.05)


#Pie Chart (Mood badge)
# Classify each mood input
mood_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
for score in cumulative_moods:
    if score >  0.05:
        mood_counts['Positive'] += 1
    elif score < -0.05:
        mood_counts['Negative'] += 1
    else:
        mood_counts['Neutral'] += 1

labels = list(mood_counts.keys())
sizes  = list(mood_counts.values())
colors = ['#99ff99', '#ffcc99', '#ff9999']
    
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title("Overall Mood Distribution")
plt.axis('equal')
    
    
plt.tight_layout()
plt.show()

print("\nComplete! Thanks for using our program.")


