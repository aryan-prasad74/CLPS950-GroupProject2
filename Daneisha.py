import os
import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Remove existing cache file to ensure fresh authentication
if os.path.exists(".cache"):
    os.remove(".cache")

# Global variable to store the Spotify client
sp = None

# This function handles when the login button is clicked
def login_clicked():
    print("Login button clicked.")
    spotify_login()  # Directly call the login function

# Function for handling the Spotify login and playlist fetching
def spotify_login():
    global sp
    print("Starting Spotify login...")

    try:
        # Set up Spotify OAuth authentication
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="95a3dd3dd0b241709a938b502eb7326a",
            client_secret="dc98f98db12d43149e4e6247a7a2fc08",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-read-private user-top-read"
        ))

        print("Fetching playlists...")
        playlists = sp.current_user_playlists()
        playlist_names = [playlist['name'] for playlist in playlists['items']]
        playlist_ids = [playlist['id'] for playlist in playlists['items']]

        print(f"Playlists fetched: {playlist_names}")

        # Directly update the UI
        show_playlist_dropdown(playlist_names, playlist_ids)

    except Exception as e:
        print(f"Error during Spotify login: {e}")

# Function to display the playlist dropdown after login
def show_playlist_dropdown(playlist_names, playlist_ids):
    print("Attempting to show dropdown menu...")

    if not playlist_names:
        print("No playlists found. Make sure the account has playlists.")
        return

    # Remove login button
    login_button.place_forget()

    # Add dropdown and label directly on root
    playlist_label = tk.Label(root, text="Select a Playlist", font=("Helvetica", 14))
    playlist_label.place(x=50, y=100)

    playlist_dropdown = ttk.Combobox(root, width=40)
    playlist_dropdown["values"] = playlist_names
    playlist_dropdown.current(0)
    playlist_dropdown.place(x=50, y=150)
    playlist_dropdown.bind("<<ComboboxSelected>>", lambda event: playlist_selected(playlist_dropdown, playlist_ids))

    # Add track listbox
    global track_list
    track_list = tk.Listbox(root, width=70, height=20)
    track_list.place(x=50, y=200)

    print("Dropdown should now be visible.")

# Function when a playlist is selected
def playlist_selected(playlist_dropdown, playlist_ids):
    print("Playlist selected.")
    selected_index = playlist_dropdown.current()
    playlist_id = playlist_ids[selected_index]

    # Fetch tracks in the selected playlist
    tracks = sp.playlist_tracks(playlist_id)
    track_list.delete(0, tk.END)  # Clear existing tracks

    for idx, item in enumerate(tracks['items'], start=1):
        track = item['track']
        track_list.insert(tk.END, f"{idx}. {track['name']} (ID: {track['id']})")

# This function creates and displays the application window for the Mood Analyzer.
def create_application_window():
    global root, login_button

    # Create main/root window
    root = tk.Tk()
    root.title("Spotify Mood Analyzer")
    root.geometry("900x700")

    # Login button directly on root
    login_button = tk.Button(root, text="Login to Spotify", command=login_clicked,
                             bg="grey", fg="black", font=("Helvetica", 14, "bold"))
    login_button.place(x=50, y=50)

    print("Application window created.")
    root.mainloop()  # Start Tkinter event loop

# If the script is being run, create the window
if __name__ == "__main__":
    create_application_window()
