# Type the following individually into terminal first #
# python3 -m pip install matplotlib
# pip install seaborn
# pip3 install 

from TotalTrackAnalyzer import profile_track_analysis

analyzed_tracks, compound_scores = profile_track_analysis()
import matplotlib.pyplot as plt
import seaborn as sns

def plot_sentiment_scores(analyzed_tracks, compound_scores):
   
    # Set the style for seaborn
    sns.set(style="whitegrid")

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 6))

    # Bar Plot
    sns.barplot(x=compound_scores, y=analyzed_tracks, ax=axs[0], palette="coolwarm")
    axs[0].set_title("Sentiment Scores per Song")
    axs[0].set_xlabel("Compound Score")
    axs[0].set_ylabel("Tracks")

    # Histogram
    sns.histplot(compound_scores, bins=20, kde=True, ax=axs[1], color='skyblue')
    axs[1].set_title("Distribution of Compound Sentiment Scores")
    axs[1].set_xlabel("Compound Score")
    axs[1].set_ylabel("Frequency")

    # Adjust layout
    plt.tight_layout()
    plt.show()

plot_sentiment_scores(analyzed_tracks, compound_scores)
