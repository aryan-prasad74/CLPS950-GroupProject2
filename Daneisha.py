import tkinter as tk
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

#Global variable to store spotify object & playlists
sp = None
playlists = []
is_analyzing = False #tracks if analysis is ongoing

#function that creates main application window
def create_application_window():
    global root, frame, welcome_label, login_button

    root = tk.Tk()
    root.title("Spotify Mood Analyzer")
    root.geometry("900x700")

    frame = tk.Frame(root)
    frame.pack(expand = True)

    #Label - welcome message
    welcome_label = tk.Label(frame, text = "Welcome to my program [test text]", font = ("Helvetica", 16), fg = "black")
    welcome_label.pack(pady = 20)

    #login button
    login_button = tk.Button(frame, text = "Analyze my Music", command = login_clicked, bg = "grey", fg = "black", font = ("Helvetica", 14, "bold"))
    login_button.pack(pady = 40)

    root.mainloop()

#function that handles spotify login and analysis
def login_and_analysis():
    global sp, playlists, is_analyzing

    if is_analyzing:
        return #prevents multiple analysis from running
    
    try:
        from TotalTrackAnalyzer import profile_track_analysis

        #sets analyzing to true
        is_analyzing = True
        
        #visual - clears frame for analysis
        frame.pack_forget()
        analysis_frame = tk.Frame(root)
        analysis_frame.pack(fill = "both", expand = True)

        analysis_label = tk.Label(analysis_frame, text = "Analyzing your music ...", font = ("Helvetica", 16), fg = "black")
        analysis_label.pack(pady = 10)

        analyzed_tracks, compound_scores = [], []

        def update_analysis(track, score):

            #update analysis UI with curr track & score
            track_label = tk.Label(analysis_frame, text = f"{track}: {score}", font = ("Helvetica", 12), fg = "black")
            track_label.pack(anchor = "w")
            root.after(0, root.update) #ensures ui refresh

        #perform analysis w/o blocking UI updates
        for track, score in profile_track_analysis(live_callback = update_analysis):
            analyzed_tracks.append(track)
            compound_scores.append(score)
            root.after(0, root.update) #visual - update UI when each track is analyzed

        #final analysis message
        complete_label = tk.Label(analysis_frame, text = "analysis complete, displaying results ...", font = ("Helvetica", 14), fg = "black")
        complete_label.pack (pady = 10)

        from ProfileAnalyticsDiagrams import plot_sentiment_scores
        plot_sentiment_scores(analyzed_tracks, compound_scores)

        #resets analysis
        is_analyzing = False

    except Exception as e:
        print("Error during Spotify login and analysis:", e)
        is_analyzing = False #resets if theres an error

#function to handle login button
def login_clicked():

    #hide welcome message and login button once clicked
    welcome_label.pack_forget()
    login_button.pack_forget()

    #starts login
    login_and_analysis()

if __name__ == "__main__":
    create_application_window()
