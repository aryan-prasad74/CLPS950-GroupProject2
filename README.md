# CLPS950-GroupProject2
For our final project we used python to program a Spotify Mood Analyzer. This code provided an application designed to allow users to analyze the sentiment of songs within their individual Spotify playlists. It is divided into several files, each handling specific tasks such as user authentication, playlist retrieval, sentiment analysis, and GUI management.
Our code does not have a fully functional user interface (UI). Although we were able to successfully develop a basic UI with one button and an application window, we encountered significant compatibility issues with macOS. These problems became apparent just before the project deadline (specifically on the Saturday before submission). Due to time constraints and technical difficulties, we decided to prioritize the core functionality of the program without relying on the UI. We have still included the UI code in the project for grading purposes.

The primary purpose of our program is to analyze a user's Spotify account by examining the lyrics of all songs in their playlists. It performs a sentiment analysis on these lyrics, assigning each song a sentiment score ranging from -1 (negative) to 1 (positive). Based on these scores, users can input a desired sentiment value within this range, and the program will generate a playlist that matches the specified sentiment. Users are able to create multiple playlists which will generate directly into their spotify account. 
To start the program, users simply need to run the code and follow the terminal prompts. Instructions can be found below.

Instructions:
Clone the repository
Navigate to the project directory
Install project dependencies using pip
    pip install spotipy OR  pip3 install spotipy
    pip install requests OR  pip3 install requests
    pip install nltk OR  pip3 install nltk
    pip install matplotlib OR  pip3 install matplotlib
    pip install seaborn OR  pip3 install seaborn
    pip install pandas OR  pip3 install pandas
    brew install python-tk
    
Since the UI is not functional, the program must be run without it. The user can do so by running the MainProgram.py document.
Users will be prompted to log into their Spotify, must use Brown email as these are the emails we have granted permissions for our Spotify application.
Once logged in, the program will begin analyzing the lyrics of all of the users spotify playlists.
After analysis, the user can input a desired sentiment score (-1 to 1) in the terminal, to generate a playlist matching that sentiment
To Note:
Our program is run through the terminal due to the UI not working properly
Some of the graph axis labels are concentrated if a user has a large number of songs in their playlists; we were unable to resolve this issue in time for the project deadline.
