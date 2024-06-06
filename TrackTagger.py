from dotenv import load_dotenv
import os
import customtkinter as ctk
import requests
from io import BytesIO
import json
import music_tag
from WelcomePage import WelcomePage
from SearchTrack import SearchTrack
from TrackConfirmation import TrackConfirmation
from TagSelection import TagSelection
from AlbumConfirmation import AlbumConfirmation
from SearchAlbum import SearchAlbum
from AlbumSelection import AlbumSelection

ENDPOINT = "https://ws.audioscrobbler.com/2.0/"

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
        welcome_page = WelcomePage(self, lambda: self.on_click_continue_welcome_page(welcome_page))
        welcome_page.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_welcome_page(self, welcome_page):
        """Collects data from welcome page and begins processing data."""
        self.directory_path = welcome_page.get_directory_path()
        self.allowed_tags = welcome_page.get_allowed_tags()
        self.denied_tags = welcome_page.get_denied_tags()
        welcome_page.destroy()

        # add all files to a list to be processed
        self.song_list = []
        self.song_index = 0
        for file in os.scandir(self.directory_path):
            if not file.is_file() or file.name[-4:] != ".mp3":
                continue

            self.song_list.append(file)

        self.process_song(None)

    def on_click_continue_search_track(self, search_track):
        """Collects data from the search track page and begins processing a song."""
        self.process_song(search_track)

    def on_click_yes_track_confirmation(self, track_confirmation):
        """Destroys the track confirmation dialog and sets up tag dialog."""
        track_confirmation.destroy()
        tag_selection = TagSelection(self, self.title, self.artist, self.tags, self.allowed_tags, self.denied_tags, lambda: self.on_click_continue_tag_selection(tag_selection))
        tag_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_no_track_confirmation(self, title_search, artist_search, track_confirmation):
        """Destroys the track confirmation dialog and moves to search track dialog."""
        track_confirmation.destroy()
        search_track = SearchTrack(self, title_search, artist_search, lambda: self.on_click_continue_search_track(search_track))
        search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_tag_selection(self, tag_selection):
        """Collects data from the tag selection dialog and proceeds to album selection."""
        self.tags = tag_selection.get_selected_tags()
        tag_selection.destroy()

        if self.album_found:
            album_confirmation = AlbumConfirmation(
                self,
                self.title,
                self.artist,
                self.album_title,
                self.album_artist,
                self.cover,
                lambda: self.on_click_yes_album_confirmation(album_confirmation),
                lambda: self.on_click_no_album_confirmation(album_confirmation)
            )
            album_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20)
        else:
            album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_continue_album_search(album_search))
            album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_yes_album_confirmation(self, album_confirmation):
        album_confirmation.destroy()
        self.write_out_metadata()

    def on_click_no_album_confirmation(self, album_confirmation):
        album_confirmation.destroy()
        album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_continue_album_search(album_search))
        album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_continue_album_search(self, album_search):
        album_title_search = album_search.get_title()
        album_search.destroy()

        parameters = {
            "method": "album.search",
            "api_key": self.key,
            "album": album_title_search,
            "format": "json"
        }
        info = requests.get(ENDPOINT, params = parameters)
        album_data = json.loads(info.text)
        self.albums = album_data["results"]["albummatches"]["album"]

        album_selection = AlbumSelection(
            self, 
            self.title, 
            self.artist, 
            self.albums, 
            lambda: self.on_click_continue_album_selection(album_selection), 
            lambda: self.on_click_back_album_selection(album_selection)
        )
        album_selection.grid(row = 0, column = 0, padx = 20, pady = 20)

    def on_click_continue_album_selection(self, album_selection):
        self.album_index = album_selection.get_album_index()
        album_selection.destroy()

        self.album_title = self.albums[self.album_index]["name"]
        self.album_artist = self.albums[self.album_index]["artist"]
    
        album_image_url = self.albums[self.album_index]["image"][-1]["#text"]
        response = requests.get(album_image_url)
        self.cover = response.content

        self.write_out_metadata()

    def on_click_back_album_selection(self, album_selection):
        album_selection.destroy()

        album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_continue_album_search(album_search))
        album_search.grid(row = 0, column = 0, padx = 20, pady = 20)

    def process_song(self, track_search):
        """Uses the last.fm API to search for track info based on title and artist."""

        if track_search is None:
            self.filepath = self.song_list[self.song_index].path
            filename = self.song_list[self.song_index].name
            title_search = filename.split(" - ")[0]
            artist_search = filename.split(" - ")[1][:-4]
        else:
            title_search = track_search.get_title()
            artist_search = track_search.get_artist()
            track_search.destroy()

        parameters = {
            "method": "track.getInfo",
            "api_key": self.key,
            "track": title_search,
            "artist": artist_search,
            "format": "json"
        }
        info = requests.get(ENDPOINT, params = parameters)
        data = json.loads(info.text)

        if "track" not in data:
            # no track found, must search 
            search_track = SearchTrack(self, title_search, artist_search, lambda: self.on_click_continue_search_track(search_track))
            search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
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
        track_confirmation = TrackConfirmation(
            self, 
            self.title, 
            self.artist, 
            playcount, 
            lambda: self.on_click_yes_track_confirmation(track_confirmation), 
            lambda: self.on_click_no_track_confirmation(title_search, artist_search, track_confirmation)
        )
        track_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def write_out_metadata(self):
        file: dict[str, str | bytes] = music_tag.load_file(self.filepath)
        file["title"] = self.title
        file["artist"] = self.artist
        file["album"] = self.album_title
        file["albumartist"] = self.album_artist
        file["artwork"] = BytesIO(self.cover).read()
        file["genre"] = self.tags
        file.save()

        self.song_index = self.song_index + 1
        self.process_song(None)

if __name__ == "__main__":
    main()
