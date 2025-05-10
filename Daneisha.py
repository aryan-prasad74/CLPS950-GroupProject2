import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk

#Remove Existing cache file to ensure problem fresh authentication
if os.path.exists(".cache"):
    os.remove(".cache")

#function to create and display application window
def create_application_window():

    #creates main/root window
    root = tk.Tk()
    root.title("Spotify Mood Analyzer")
    root.geometry("900x800")

    frame = tk.Frame(root)
    frame.pack(expand = True)

    global login_button
    login_button = tk.Button(frame, text = "Login to Spotify", command = login_clicked,
                             bg = "grey", fg = "black", font = ("Helvetica", 14, "bold"))
    login_button.pack(pady = 40)

    #dropdown label
    global playlist_label
    playlist_label = tk.Label(frame, text = "Select a Playlist", font = ("Helcetica", 14))

    #dropdown menu
    global playlist_dropdown
    playlist_dropdown = ttk.Combobox(frame, width = 40)
    playlist_dropdown.bind("<<ComboboxSelected>>", playlist_selected)

    root.mainloop()

#function handles when login button is clicked
def login_clicked():
    
    #Spotify OAuth authentication setup; User input credentials and redirect URI (TEST(G))
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
        client_id = "95a3dd3dd0b241709a938b502eb7326a",
        client_secret = "dc98f98db12d43149e4e6247a7a2fc08",
        redirect_uri = "http://127.0.0.1:8888/callback",
        scope = "playlist-read-private user-top-read"
    ))

    #List playlists
    playlists = sp.current_user_playlists()
    playlist_names = [playlist['name'] for playlist in playlists['items']]

    #dropdown menu with playlist names
    playlist_dropdown["values"] = playlist_names
    playlist_dropdown.set("Select a Playlist")

    #hide login button, show dropdown
    login_button.pack_forget()
    playlist_label.pack(pady = 20)
    playlist_dropdown.pack(pady = 10)

#function for when a playlist is selected from the dropdown
def playlist_selected(event):
    selected_playlist = playlist_dropdown.get()
    print(f"Selected Playlist: {selected_playlist}")

if __name__ == "__main__":
    create_application_window()