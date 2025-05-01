import tkinter as tk

#This function handles when the login button is clicked
def login_clicked():
    print("login button clicked") #placeholder, replace w authentication code

    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    # Set your credentials and redirect URI --- TEST(G)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="95a3dd3dd0b241709a938b502eb7326a",
        client_secret="dc98f98db12d43149e4e6247a7a2fc08",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope= "playlist-read-private user-top-read"
    ))

    ## List playlists
    playlists = sp.current_user_playlists()
    for idx, playlist in enumerate(playlists['items'], start=1):
        print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

    # Prompt the user to select a playlist by index
    selected_index = int(input("\nEnter the index of the playlist to view its tracks: ")) - 1
    selected_playlist_id = playlists['items'][selected_index]['id']

    # Fetch the tracks in the selected playlist
    tracks = sp.playlist_tracks(selected_playlist_id)

    print(f"\nTracks in playlist '{playlists['items'][selected_index]['name']}':")
    cumulative_ids = []
    for idx, item in enumerate(tracks['items'], start=1):
        track = item['track']
        print(f"{idx}. {track['name']} (ID: {track['id']})")
        cumulative_ids.append(track['id'])
    print(cumulative_ids)


#This function creates and displays the application window for the Mood Analyzer.
def create_application_window():

    #creates main / root window 
    root = tk.Tk()
    root.title("Spotify Mood Analyzer")
    root.geometry("900x700")

    #creates frame within the window for layout
    frame = tk.Frame(root)
    frame.pack(expand = True)

    #creates login button within the frame
    login_button = tk.Button(frame, text = "Login to Spotify", command = login_clicked,
                             bg = "grey", fg = "black", font = ("Helvetica", 14, "bold"))
    login_button.pack(pady = 40)

    root.mainloop() #this line of code starts the tkinter event loop, which will keep the window open and working

#if the script is being run, create the window
if __name__ == "__main__":
    create_application_window()