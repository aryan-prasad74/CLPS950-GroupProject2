import os

from Jamin import profile_track_analysis
from PlaylistAnalyze import sp
from ProfileAnalyticsDiagrams import plot_sentiment_scores
from TotalTrackAnalyzer import profile_track_analysis as analyze_tracks

#clear cache
if os.path.exists(".cache"):
    os.remove(".cache")

print("Starting Spotify Mood Analysis Program")

#run profile track analysis
print("\nRunning Track Analysis ...")
analyzed_tracks, compound_scores = analyze_tracks()

# #run playlist analysis
# print("\nRunning Playlist Analyzer ...")
# playlists = sp.current_user_playlists()
# for idx, playlist in enumerate(playlists['items'], start=1):
#     print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

# #run diagrams
# print("\nRunning Analytic Diagrams ...")
# plot_sentiment_scores(analyzed_tracks, compound_scores)

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