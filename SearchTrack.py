import customtkinter as ctk

class SearchTrack(ctk.CTkFrame):
    """Holds the UI for searching for a track by title and artist."""

    def __init__(self, master, title, artist, on_click_continue, invalid_search = False):
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
        on_click_continue: Callable[]
            Defines on-click behavior for the continue button.
        invalid_search: boolean
            True if either search criteria is blank or no results are found.
        """
        super().__init__(master)

        # center items horizontally
        self.grid_columnconfigure(0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"Track {title} by {artist} not found. Please search for a track.")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.title = ctk.CTkEntry(master = self, width = 400, placeholder_text = "title")
        self.title.grid(row = 1, column = 0, padx = 20, sticky = "w")

        self.artist = ctk.CTkEntry(master = self, width = 400, placeholder_text = "artist")
        self.artist.grid(row = 2, column = 0, padx = 20, pady = (5, 0), sticky = "w")

        self.continue_button = ctk.CTkButton(master = self, text = "continue", command = on_click_continue)
        self.continue_button.grid(row = 3, column = 0, pady = 20)

        if invalid_search:
            self.invalid_search_label = ctk.CTkLabel(master = self, text = f"Please provide valid search criteria.", text_color = "red")
            self.invalid_search_label.grid(row = 4, column = 0, padx = 20, pady = (0, 20), sticky = "w")

    def get_title(self):
        return self.title.get()

    def get_artist(self):
        return self.artist.get()
