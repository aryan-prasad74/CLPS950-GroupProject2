import tkinter as tk

#This function handles when the login button is clicked
def login_clicked():
    print("login button clicked") #placeholder, replace w authentication code

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