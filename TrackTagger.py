from dotenv import load_dotenv
import os
import customtkinter as ctk
import requests
import urllib.parse
import json
from WelcomePage import WelcomePage
from SearchTrack import SearchTrack
from TrackConfirmation import TrackConfirmation
from TagSelection import TagSelection

ENDPOINT = "https://ws.audioscrobbler.com/2.0/?method="

def main():
    load_dotenv()
    key = os.environ["KEY"]

    app = Application(key)
    app.mainloop()

class Application(ctk.CTk):
    """The base application class for CTkinter that holds the entire UI."""

    def __init__(self, key):
        """Initializes window size, title, and display welcome page."""
        super().__init__()
        self.key = key

        self.geometry("800x800")
        self.title("TrackTagger")
        self.grid_columnconfigure(0, weight = 1)

        self.display_welcome_page()

    def display_welcome_page(self):
        """Displays a frame to collect the directory path and tag lists."""
        self.welcome_page = WelcomePage(self, self.on_click_continue_welcome_page)
        self.welcome_page.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_welcome_page(self):
        """Collects data from welcome page and begins processing data."""
        self.directory_path = self.welcome_page.get_directory_path()
        self.allowed_tags = self.welcome_page.get_allowed_tags()
        self.denied_tags = self.welcome_page.get_denied_tags()
        self.welcome_page.destroy()
        self.process_song("Dust in the Wind", "Kansas")

    def on_click_continue_search_track(self):
        """Collects data from the search track page and begins processing a song."""
        title_search = self.search_track.get_title()
        artist_search = self.search_track.get_artist()
        self.process_song(title_search, artist_search)

    def on_click_yes_track_confirmation(self):
        """Destroys the track confirmation dialog and sets up tag dialog."""
        self.track_confirmation.destroy()
        self.tag_selection = TagSelection(self, self.title, self.artist, self.tags, self.allowed_tags, self.denied_tags, None)
        self.tag_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def process_song(self, title_search, artist_search):
        """Uses the last.fm API to search for track info based on title and artist."""
        info = requests.get(f"{ENDPOINT}track.getInfo&api_key={self.key}&track={urllib.parse.quote_plus(title_search)}&artist={urllib.parse.quote_plus(artist_search)}&format=json")
        data = json.loads(info.text)

        if "track" not in data:
            # no track found, must search
            self.search_track = SearchTrack(self, title_search, artist_search, None)
            self.search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        self.title = data["track"]["name"]
        self.artist = data["track"]["artist"]["name"]
        playcount = data["track"]["playcount"]
        
        self.tags = []
        for tag in data["track"]["toptags"]["tag"]:
            self.tags.append(tag["name"].lower())

        # display confirmation page for this track
        self.track_confirmation = TrackConfirmation(self, self.title, self.artist, playcount, self.on_click_yes_track_confirmation, None)
        self.track_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

        # todo: tag dialog
        # todo: album dialog (if album found)

if __name__ == "__main__":
    main()
