# def summary_diagrams():
#     return #ADD DIAGRAM NAMES
######################################################################

import tkinter as tk
import threading
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


# Global variable to store Spotify object and playlists
sp = None
playlists = []


# Function to handle Spotify login
def login_to_spotify():
   global sp, playlists
   try:
    # Spotify OAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="37c9bce1cdbc4583b26bd65253b04a36",
        client_secret="4067ab6c82a1422289c534641e81d9c4",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="playlist-read-private user-top-read"
    ))


   except Exception as e:
       print("Error during Spotify login:", e)




# Function to handle login button click
def login_clicked():
   threading.Thread(target=login_to_spotify).start()


# Function to create the main application window
def create_application_window():
   global root, login_button


   root = tk.Tk()
   root.title("Spotify Mood Analyzer")
   root.geometry("900x700")


   frame = tk.Frame(root)
   frame.pack(expand=True)


   login_button = tk.Button(frame, text="Login to Spotify", command=login_clicked, bg="grey", fg="black", font=("Helvetica", 14, "bold"))
   login_button.pack(pady=40)


   root.mainloop()


# If the script is being run, create the window
if __name__ == "__main__":
   create_application_window()