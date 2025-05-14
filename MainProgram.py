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
profile_track_analysis

#run playlist analysis
print("\nRunning Playlist Analyzer ...")
playlists = sp.current_user_playlists()
for idx, playlist in enumerate(playlists['items'], start=1):
    print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

#run total track analysis
print("\nRunning Total Track Analysis ...")
analyzed_tracks, compound_scores = analyze_tracks()

#run diagrams
print("\nRunning Analytic Diagrams ...")
plot_sentiment_scores(analyzed_tracks, compound_scores)

print("\nComplete! Thanks for using our program.")