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


# Mood Badge (Pie Chart)
# Define mood categories
positive = sum(1 for score in compound_scores if score > 0.05)
neutral = sum(1 for score in compound_scores if -0.05 <= score <= 0.05)
negative = sum(1 for score in compound_scores if score < -0.05)

# Data for pie chart
labels = ['Positive', 'Neutral', 'Negative']
sizes = [positive, neutral, negative]
colors = ['green', 'grey', 'red']

# Create pie chart
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Mood Distribution in Final Playlist')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# Plotting mood over time (Using data from CSV File)
df = pd.read_csv(filename, names=['Timestamp', 'Average_Score'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.sort_values('Timestamp', inplace=True)

plt.figure(figsize=(10, 5))
plt.plot(df['Timestamp'], df['Average_Score'], marker='o', linestyle='-')
plt.title('Average Sentiment Score Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Average Sentiment Score')
plt.grid(True)
plt.tight_layout()
plt.show()


print("\nComplete! Thanks for using our program.")