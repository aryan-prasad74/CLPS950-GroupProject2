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
       # Spotify authentication using Spotipy
       sp = Spotify(auth_manager=SpotifyOAuth(
           client_id="YOUR_CLIENT_ID",
           client_secret="YOUR_CLIENT_SECRET",
           redirect_uri="http://127.0.0.1:8888/callback",
           scope="playlist-read-private user-top-read"
       ))


       # Fetch user playlists
       playlists_data = sp.current_user_playlists()
       playlists = [p['name'] for p in playlists_data['items']]


       # Update UI after login
       update_ui_after_login()


   except Exception as e:
       print("Error during Spotify login:", e)


# Function to update UI after login
def update_ui_after_login():
   login_button.pack_forget()  # Remove login button


   # Create dropdown for playlists
   playlist_var.set("Select a Playlist")
   playlist_dropdown.pack(pady=10)


   # Populate dropdown menu
   playlist_dropdown['menu'].delete(0, 'end')
   for playlist in playlists:
       playlist_dropdown['menu'].add_command(label=playlist, command=lambda p=playlist: playlist_var.set(p))


# Function to handle login button click
def login_clicked():
   threading.Thread(target=login_to_spotify).start()


# Function to create the main application window
def create_application_window():
   global root, login_button, playlist_var, playlist_dropdown


   root = tk.Tk()
   root.title("Spotify Mood Analyzer")
   root.geometry("900x700")


   frame = tk.Frame(root)
   frame.pack(expand=True)


   tk.Label(frame, text="Hello and welcome to our Spotify Mood Analyzer.", font=("Helvetica", 16, "bold"), fg="black", wraplength=600).pack(pady=10)
   tk.Label(frame, text="This program will take information from all existing and saved playlists on your account to generate a playlist based on the mood you pick.", wraplength=600, font=("Helvetica", 12), fg="black").pack(pady=10)


   login_button = tk.Button(frame, text="Login to Spotify", command=login_clicked, bg="grey", fg="black", font=("Helvetica", 14, "bold"))
   login_button.pack(pady=20)


   # Dropdown for playlists
   playlist_var = tk.StringVar()
   playlist_dropdown = tk.OptionMenu(frame, playlist_var, "Loading...")


   root.mainloop()


# If the script is being run, create the window
if __name__ == "__main__":
   create_application_window()
