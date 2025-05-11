import tkinter as tk
import threading as threading
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Global variable to store Spotify object and playlists
sp = None
playlists = []


# STEP 1: LOGIN BUTTON - Authenticate, Analyse Music, and Display Graphs

# Function to handle Spotify login
def login_to_spotify():
   global sp, playlists
   try:
      from TotalTrackAnalyzer import profile_track_analysis
      analyzed_tracks, compound_scores = profile_track_analysis()
   except Exception as e:
       print("Error during Spotify login:", e)

# Function to handle login button click
def login_clicked():
#  welcome_label.pack_forget()  # Hide welcome message
   threading.Thread(target=login_to_spotify).start()
   root.mainloop()

# STEP 2: DISPLAY ANALYTICS DIAGRAMS
   from ProfileAnalyticsDiagrams import plot_sentiment_scores
   plot_sentiment_scores(analyzed_tracks, compound_scores)
# Display diagrams on UI

##############################################################################################################################################################################
##############################################################################################################################################################################

# Function to create the main application window
def create_application_window():
   global root, login_button #When add buttons, add here#
   root = tk.Tk()
   root.title("Spotify Mood Analyzer")
   root.geometry("900x700")

   frame = tk.Frame(root)
   frame.pack(expand=True)

# Display Label (Welcome message)
   welcome_label = tk.Label(frame, text="Welcome message", font=("Helvetica", 16), fg="black")
   welcome_label.pack(pady=20)

# Create Login Button (Step 1)
   login_button = tk.Button(frame, text="Login to Spotify", command=login_clicked, bg="grey", fg="black", font=("Helvetica", 14, "bold"))
   login_button.pack(pady=40)

# Create "Analyse my Music" Button (Step 2)
#   login_button = tk.Button(frame, text="Analyse my Music", command=login_clicked, bg="grey", fg="black", font=("Helvetica", 14, "bold"))
#   login_button.pack(pady=40)

   root.mainloop()

##############################################################################################################################################################################
##############################################################################################################################################################################
## DON'T MOVE, DON'T CHANGE ##
# If the script is being run, create the window
if __name__ == "__main__":
   create_application_window()
