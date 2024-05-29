from dotenv import load_dotenv
import os
import customtkinter as ctk
from WelcomePage import WelcomePage

ENDPOINT = "https://ws.audioscrobbler.com/2.0/?method="

def main():
    load_dotenv()
    key = os.environ["KEY"]

    app = Application()
    app.mainloop()

class Application(ctk.CTk):
    """ The base application class for CTkinter that holds the entire UI. """

    def __init__(self):
        """ Initializes window size, title, and display welcome page. """
        super().__init__()
        self.geometry("800x800")
        self.title("TrackTagger")
        self.grid_columnconfigure(0, weight = 1)

        self.displayWelcomePage()

    def displayWelcomePage(self):
        """ Displays a frame to collect the directory path and tag lists. """
        self.welcomePage = WelcomePage(self, self.onClickContinueWelcomePage)
        self.welcomePage.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def onClickContinueWelcomePage(self):
        """ Collects data from welcome page and begins processing data. """
        self.directoryPath = self.welcomePage.get_directory_path()
        self.allowedTags = self.welcomePage.get_allowed_tags()
        self.deniedTags = self.welcomePage.get_denied_tags()
        self.welcomePage.destroy()

if __name__ == "__main__":
    main()
