import customtkinter as ctk

class ManualAlbumUpdate(ctk.CTkFrame):
    """Holds the UI to display dialog options for album artist and album cover."""

    def __init__(self, master, title, artist, album_title, on_click_update, on_click_back, invalid = False, invalid_path = False):
        """
        Initializes UI components.

        Parameters
        ----------
        master: CTk | CTkFrame
            The parent container of this frame.
        title: str
            The title of the current track.
        artist: str
            The artist of the current track.
        album_title: str
            The album title of the current track.
        on_click_update: Callable[]
            Defines on-click behavior for the update button.
        on_click_back: Callable[]
            Defines on-click behavior for the back button.
        invalid: boolean
           True if either the album artist or cover path were empty on update. 
        invalid_path: boolean
            True if the provided file path for album cover was invalid on update.
        """
        super().__init__(master)

        # center items horizontally
        self.columnconfigure(index = 0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"The current track is {title} by {artist} and the current album is {album_title}.\nPlease enter an album artist and album cover or go back to the search page.", anchor = "w", justify = "left")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.album_artist = ctk.CTkEntry(master = self, width = 400, placeholder_text = "album artist")
        self.album_artist.insert(0, artist)
        self.album_artist.grid(row = 1, column = 0, padx = 20, sticky = "w")

        self.album_cover_path = ctk.CTkEntry(master = self, width = 400, placeholder_text = "/path/to/cover.png")
        self.album_cover_path.grid(row = 2, column = 0, padx = 20, pady = (5, 20), sticky = "w")

        self.sub_frame = ctk.CTkFrame(self)
        self.sub_frame.grid(row = 3, column = 0, padx = 20, pady = (0, 20))

        self.back_button = ctk.CTkButton(master = self.sub_frame, text = "back", command = on_click_back)
        self.back_button.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.update_button = ctk.CTkButton(master = self.sub_frame, text = "update", command = on_click_update)
        self.update_button.grid(row = 0, column = 1, padx = 20, pady = 20)

        if invalid:
            self.invalid_label = ctk.CTkLabel(master = self, text = f"Please enter valid criteria for album artist and cover path.", text_color = "red")
            self.invalid_label.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "w")
        elif invalid_path:
            self.invalid_path_label = ctk.CTkLabel(master = self, text = f"Invalid album cover path.", text_color = "red")
            self.invalid_path_label.grid(row = 4, column = 0, padx = 20, pady = 20, sticky = "w")
                

    def get_album_artist(self):
        return self.album_artist.get()

    def get_album_cover_path(self):
        return self.album_cover_path.get()
