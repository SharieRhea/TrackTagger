import customtkinter as ctk

class SearchTrack(ctk.CTkFrame):
    """Holds the UI for searching for a track by title and artist."""

    def __init__(self, master, title, artist, filename, on_click_update, on_click_search, invalid = False):
        """
        Initializes UI components.

        Parameters
        ----------
        master: CTk | CTkFrame
            Parent container of this frame.
        title: str
            The title of the track that couldn't be found.
        artist: str
            The artist of the track that couldn't be found.
        on_click_update: Callable[]
            Defines on-click behavior for the update button.
        on_click_search: Callable[]
            Defines on-click behavior for the search button.
        invalid: boolean
            True if either search criteria is blank or no results are found.
        """
        super().__init__(master)

        # center items horizontally
        self.grid_columnconfigure(0, weight = 1)

        if title == "" or artist == "":
            self.message_label = ctk.CTkLabel(master = self, text = f"Could not search for file {filename}. Please search for a track or update the title and artist manually.")
        else:
            self.message_label = ctk.CTkLabel(master = self, text = f"Track {title} by {artist} not found. Please search for a track or update title and artist manually.")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.title = ctk.CTkEntry(master = self, width = 400, placeholder_text = "title")
        self.title.grid(row = 1, column = 0, padx = 20, sticky = "w")
        self.title.focus_set()

        self.artist = ctk.CTkEntry(master = self, width = 400, placeholder_text = "artist")
        self.artist.grid(row = 2, column = 0, padx = 20, pady = (5, 20), sticky = "w")

        self.sub_frame = ctk.CTkFrame(self)
        self.sub_frame.grid(row = 3, column = 0, padx = 20, pady = (0, 20))

        self.update_button = ctk.CTkButton(master = self.sub_frame, text = "update", command = on_click_update)
        self.update_button.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.search_button = ctk.CTkButton(master = self.sub_frame, text = "search", command = on_click_search)
        self.search_button.grid(row = 0, column = 1, padx = 20, pady = 20)

        if invalid:
            self.invalid_label = ctk.CTkLabel(master = self, text = f"Please provide valid criteria.", text_color = "red")
            self.invalid_label.grid(row = 4, column = 0, padx = 20, pady = (0, 20), sticky = "w")

    def get_title(self):
        return self.title.get()

    def get_artist(self):
        return self.artist.get()
