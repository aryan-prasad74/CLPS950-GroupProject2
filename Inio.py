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

#run diagrams
print("\nRunning Analytic Diagrams ...")
plot_sentiment_scores(analyzed_tracks, compound_scores)

print("\nComplete! Thanks for using our program.")