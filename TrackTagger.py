from dotenv import load_dotenv
import os
import re
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
from ManualAlbumUpdate import ManualAlbumUpdate

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
        
        # need to provide a directory, cannot be blank
        if self.directory_path == "":
            welcome_page.destroy()
            welcome_page = WelcomePage(self, lambda: self.on_click_continue_welcome_page(welcome_page), invalid_directory = True)
            welcome_page.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        # user omitted the trailing slash, add it
        if self.directory_path[-1] != '/':
            self.directory_path += '/'
        
        # check if it is a valid directory
        if not os.path.isdir(self.directory_path):
            welcome_page.destroy()
            welcome_page = WelcomePage(self, lambda: self.on_click_continue_welcome_page(welcome_page), invalid_directory = True)
            welcome_page.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return
            
        self.allowed_tags = set(welcome_page.get_allowed_tags().split(", "))
        self.denied_tags = set(welcome_page.get_denied_tags().split(", "))
        welcome_page.destroy()

        # add all files to a list to be processed
        self.song_list = []
        self.song_index = 0
        for file in os.scandir(self.directory_path):
            if not file.is_file() or file.name[-4:] != ".mp3":
                continue

            self.song_list.append(file)

        self.process_song(None)

    def on_click_search_search_track(self, search_track):
        """Collects data from the search track page and begins processing a song."""
        self.process_song(search_track)

    def on_click_update_search_track(self, search_track):
        """Collects data from the search track page and sets the title and artist. Moves immediately to album search."""
        self.title = search_track.get_title()
        self.artist = search_track.get_artist()
        search_track.destroy()

        # check for invalid input
        if self.title == "" or self.artist == "":
            search_track = SearchTrack(self, "", "", self.filename, lambda: self.on_click_update_search_track(search_track), lambda: self.on_click_search_search_track(search_track), invalid = True)
            search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        self.tags = []
        self.album_found = False
        tag_selection = TagSelection(self, self.title, self.artist, self.tags, self.allowed_tags, self.denied_tags, lambda: self.on_click_continue_tag_selection(tag_selection))
        tag_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_yes_track_confirmation(self, track_confirmation):
        """Destroys the track confirmation dialog and sets up tag dialog."""
        track_confirmation.destroy()
        tag_selection = TagSelection(self, self.title, self.artist, self.tags, self.allowed_tags, self.denied_tags, lambda: self.on_click_continue_tag_selection(tag_selection))
        tag_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_no_track_confirmation(self, title_search, artist_search, track_confirmation):
        """Destroys the track confirmation dialog and moves to search track dialog."""
        track_confirmation.destroy()
        search_track = SearchTrack(self, title_search, artist_search, self.filename, lambda: self.on_click_update_search_track(search_track), lambda: self.on_click_search_search_track(search_track))
        search_track.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_tag_selection(self, tag_selection):
        """Collects data from the tag selection dialog and proceeds to album selection."""
        self.tags = tag_selection.get_selected_tags()

        # add tags to the allowed list so they are auto-selected in the future
        for tag in self.tags:
            self.allowed_tags.add(tag)

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
            album_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
        else:
            album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search))
            album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_yes_album_confirmation(self, album_confirmation):
        album_confirmation.destroy()
        self.write_out_metadata()

    def on_click_no_album_confirmation(self, album_confirmation):
        album_confirmation.destroy()
        album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search))
        album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_update_album_search(self, album_search):
        self.album_title = album_search.get_title()
        album_search.destroy()

        if self.album_title == "":
            album_search = SearchAlbum(
                self, 
                self.title, 
                self.artist, 
                lambda: self.on_click_update_album_search(album_search), 
                lambda: self.on_click_search_album_search(album_search), 
                invalid = True
            )
            album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        manual_album_update = ManualAlbumUpdate(
            self, 
            self.title, 
            self.artist, 
            self.album_title, 
            lambda: self.on_click_update_manual_album_update(manual_album_update),
            lambda: self.on_click_back_manual_album_update(manual_album_update),
        )
        manual_album_update.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_search_album_search(self, album_search):
        album_title_search = album_search.get_title()
        album_search.destroy()

        if album_title_search == "":
            album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search), invalid = True)
            album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        parameters = {
            "method": "album.search",
            "api_key": self.key,
            "album": album_title_search,
            "format": "json"
        }
        info = requests.get(ENDPOINT, params = parameters)
        album_data = json.loads(info.text)
        
        # no albums found for given search criteria
        if "results" not in album_data:
            album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search), invalid = True)
            album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        # FIX: crashes here if no album was present in results
        self.albums = album_data["results"]["albummatches"]["album"]

        album_selection = AlbumSelection(
            self, 
            self.title, 
            self.artist, 
            self.albums, 
            lambda: self.on_click_continue_album_selection(album_selection), 
            lambda: self.on_click_back_album_selection(album_selection)
        )
        album_selection.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_update_manual_album_update(self, manual_album_update):
        self.album_artist = manual_album_update.get_album_artist()
        album_cover_path = manual_album_update.get_album_cover_path()
        manual_album_update.destroy()

        if self.album_artist == "" or album_cover_path == "":
            manual_album_update = ManualAlbumUpdate(
                self, 
                self.title, 
                self.artist, 
                self.album_title, 
                lambda: self.on_click_update_manual_album_update(manual_album_update),
                lambda: self.on_click_back_manual_album_update(manual_album_update),
                invalid = True
            )
            manual_album_update.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        # figure out if album cover path is actually an image file
        if not os.path.isfile(album_cover_path):
            manual_album_update = ManualAlbumUpdate(
                self, 
                self.title, 
                self.artist, 
                self.album_title, 
                lambda: self.on_click_update_manual_album_update(manual_album_update),
                lambda: self.on_click_back_manual_album_update(manual_album_update),
                invalid_path = True
            )
            manual_album_update.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
            return

        with open(album_cover_path, 'rb') as image:
            self.cover = image.read()
            self.write_out_metadata()
               
    def on_click_back_manual_album_update(self, manual_album_update):
        manual_album_update.destroy()
        album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search))
        album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def on_click_continue_album_selection(self, album_selection):
        self.album_index = album_selection.get_album_index()
        album_selection.destroy()

        self.album_title = self.albums[self.album_index]["name"]
        self.album_artist = self.albums[self.album_index]["artist"]
    
        album_image_url = self.albums[self.album_index]["image"][-1]["#text"]
        try:
            response = requests.get(album_image_url)
            self.cover = response.content
        except requests.exceptions.MissingSchema:
            self.cover = None

        self.write_out_metadata()

    def on_click_back_album_selection(self, album_selection):
        album_selection.destroy()

        album_search = SearchAlbum(self, self.title, self.artist, lambda: self.on_click_update_album_search(album_search), lambda: self.on_click_search_album_search(album_search))
        album_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

    def process_song(self, track_search):
        """First, checks to see if there is existing metadata. Next, uses the last.fm API to search for track info based on title and artist."""

        if self.song_index >= len(self.song_list):
            if track_search is not None:
                track_search.destroy()
            thank_you_message = ctk.CTkLabel(master = self, text = "Thank you for using TrackTagger!", font = ("", 20))
            thank_you_message.grid(row = 0, column = 0, padx = 20, pady = 20)
            return

        if track_search is None:
            self.filepath = self.song_list[self.song_index].path
            self.filename = self.song_list[self.song_index].name

            # check existing metadata for title and artist
            file = music_tag.load_file(self.filepath)
            title = str(file["title"])
            artist = str(file["artist"])
            # if present, no need to search, just ask user to verify
            if title != "" and artist != "":
                track_confirmation = TrackConfirmation(
                    self, 
                    title, 
                    artist, 
                    -1, 
                    lambda: self.on_click_yes_track_confirmation(track_confirmation), 
                    lambda: self.on_click_no_track_confirmation(title, artist, track_confirmation)
                )
                track_confirmation.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
                return

            # see if filename is formatted for last.fm search
            if " - " in self.filename:
                title_search = self.filename.split(" - ")[0]
                artist_search = self.filename.split(" - ")[1][:-4]
            else:
                filename = self.song_list[self.song_index].name
                track_search = SearchTrack(self, "", "", self.filename, lambda: self.on_click_update_search_track(track_search), lambda: self.on_click_search_search_track(track_search))
                track_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
                return

        else:
            title_search = track_search.get_title()
            artist_search = track_search.get_artist()
            track_search.destroy()

            if title_search == "" or artist_search == "":
                filename = self.song_list[self.song_index].name
                track_search = SearchTrack(
                    self, 
                    filename.split(" - ")[0], 
                    filename.split(" - ")[1][:-4], 
                    self.filename,
                    lambda: self.on_click_update_search_track(track_search),
                    lambda: self.on_click_search_search_track(track_search), 
                    invalid = True
                )
                track_search.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")
                return

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
            search_track = SearchTrack(
                self, 
                title_search, 
                artist_search, 
                self.filename, 
                lambda: self.on_click_update_search_track(search_track), 
                lambda: self.on_click_search_search_track(track_search)
            )
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
            if album_image_url != "":
                response = requests.get(album_image_url)
                self.cover = response.content
            else:
                self.cover = None
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
        file = music_tag.load_file(self.filepath)
        file["title"] = self.title
        file["artist"] = self.artist
        file["album"] = self.album_title
        file["albumartist"] = self.album_artist
        if self.cover is not None:
            file["artwork"] = BytesIO(self.cover).read()
        file["genre"] = self.tags
        file.save()

        # remove illegal filepath characters from the title and artist before renaming
        os.rename(self.filepath, f"{self.directory_path}{re.sub('[\\/:*?"<>|]', '', self.title)} - {re.sub('[\\/:*?"<>|]', '', self.artist)}.mp3")
        self.song_index = self.song_index + 1
        self.process_song(None)

if __name__ == "__main__":
    main()
