from dotenv import load_dotenv
import os
import customtkinter as ctk
import requests
from io import BytesIO
import urllib.parse
import json
import music_tag
from WelcomePage import WelcomePage
from SearchTrack import SearchTrack
from TrackConfirmation import TrackConfirmation
from TagSelection import TagSelection
from AlbumConfirmation import AlbumConfirmation
from SearchAlbum import SearchAlbum
from AlbumSelection import AlbumSelection

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

        # begin processing every song in the directory
        for file in os.scandir(self.directory_path):
            if not file.is_file() or file.name[-4:] != ".mp3":
                continue

            info = file.name.split(" - ")
            self.filepath = file.path
            self.process_song(info[0], info[1][:-4])

    def on_click_continue_search_track(self):
        """Collects data from the search track page and begins processing a song."""
        self.title_search = self.search_track.get_title()
        self.artist_search = self.search_track.get_artist()
        self.process_song(self.title_search, self.artist_search)

    def on_click_yes_track_confirmation(self):
        """Destroys the track confirmation dialog and sets up tag dialog."""
        self.track_confirmation.destroy()
        self.tag_selection = TagSelection(self, self.title, self.artist, self.tags, self.allowed_tags, self.denied_tags, self.on_click_continue_tag_selection)
        self.tag_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_no_track_confirmation(self):
        """Destroys the track confirmation dialog and moves to search track dialog."""
        self.track_confirmation.destroy()
        self.search_track = SearchTrack(self, self.title_search, self.artist_search, None)
        self.search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_tag_selection(self):
        """Collects data from the tag selection dialog and proceeds to album selection."""
        self.tags = self.tag_selection.get_selected_tags()
        self.tag_selection.destroy()

        if self.album_found:
            self.album_confirmation = AlbumConfirmation(self, self.title, self.artist, self.album_title, self.album_artist, self.cover, self.on_click_yes_album_confirmation, self.on_click_no_album_confirmation)
            self.album_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20)
        else:
            self.album_search = SearchAlbum(self, self.title, self.artist, self.on_click_continue_album_search)
            self.album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_yes_album_confirmation(self):
        self.album_confirmation.destroy()

        self.write_out_metadata(self.filepath, self.title, self.artist, self.album_title, self.album_artist, self.cover, self.tags)

    def on_click_no_album_confirmation(self):
        self.album_confirmation.destroy()
        self.album_search = SearchAlbum(self, self.title, self.artist, self.on_click_continue_album_search)
        self.album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_continue_album_search(self):
        album_title_search = self.album_search.get_title()
        self.album_search.destroy()

        info = requests.get(f"{ENDPOINT}album.search&api_key={self.key}&album={urllib.parse.quote_plus(album_title_search)}&format=json")
        album_data = json.loads(info.text)
        self.albums = album_data["results"]["albummatches"]["album"]

        self.album_selection = AlbumSelection(self, self.title, self.artist, self.albums, self.on_click_continue_album_selection, self.on_click_back_album_selection)
        self.album_selection.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_continue_album_selection(self):
        self.album_index = self.album_selection.get_album_index()
        self.album_selection.destroy()

        self.album_title = self.albums[self.album_index]["name"]
        self.album_artist = self.albums[self.album_index]["artist"]
    
        album_image_url = self.albums[self.album_index]["image"][-1]["#text"]
        response = requests.get(album_image_url)
        self.cover = response.content

        self.write_out_metadata(self.filepath, self.title, self.artist, self.album_title, self.album_artist, self.cover, self.tags)

    def on_click_back_album_selection(self):
        self.album_selection.destroy()

        self.album_search = SearchAlbum(self, self.title, self.artist, self.on_click_continue_album_search)
        self.album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def process_song(self, title_search, artist_search):
        """Uses the last.fm API to search for track info based on title and artist."""
        # todo: replace this with the better dictionary syntax for parameters
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

        if "album" in data["track"]:
            self.album_found = True
            self.album_title = data["track"]["album"]["title"]
            self.album_artist = data["track"]["album"]["artist"]
            album_image_url = data["track"]["album"]["image"][-1]["#text"]
            response = requests.get(album_image_url)
            self.cover = response.content
        else:
            self.album_found = False

        # display confirmation page for this track
        self.track_confirmation = TrackConfirmation(self, self.title, self.artist, playcount, self.on_click_yes_track_confirmation, self.on_click_no_track_confirmation)
        self.track_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def write_out_metadata(self, filepath, title, artist, album_title, album_artist, cover, tags):
        file: dict[str, str | bytes] = music_tag.load_file(filepath)
        file["title"] = title
        file["artist"] = artist
        file["album"] = album_title
        file["albumartist"] = album_artist
        file["artwork"] = BytesIO(cover).read()
        file["genre"] = tags
        file.save()

if __name__ == "__main__":
    main()
