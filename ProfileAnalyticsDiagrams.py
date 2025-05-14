# Type the following individually into the terminal:
# python3 -m pip install matplotlip OR python3 -m pip3 install matplotlip
# pip install seaborn OR pip3 install seaborn
# pip3 install

import matplotlib.pyplot as plt
import seaborn as sns

#Import the profile_track_analysis function from TotalTrackAnalyzer
from TotalTrackAnalyzer import profile_track_analysis

#Execute track analyssi function - this returns analyzed tracks and their sentiment scores
analyzed_tracks, compound_scores = profile_track_analysis()

#Function to visualize sentiment scores
def plot_sentiment_scores(analyzed_tracks, compound_scores):
    
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

#Call function
plot_sentiment_scores(analyzed_tracks, compound_scores)