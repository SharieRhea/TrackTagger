import customtkinter as ctk

class SearchAlbum(ctk.CTkFrame):
    """Holds the UI for searching for an album by title and artist."""

    def __init__(self, master, title, artist, on_click_continue, invalid_search = False):
        """
        Initializes UI components.

        Parameters
        ----------
        master: CTk | CTkFrame
            Parent container of this frame.
        title: str
            The title of the current track.
        artist: str
            The artist of the current track. 
        on_click_continue: Callable[]
            Defines on-click behavior for the continue button.
        invalid_search: boolean
            True if the title search was empty on continue.
        """
        super().__init__(master)

        # center items horizontally
        self.grid_columnconfigure(0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"The current track is {title} by {artist}. Please search for an album.")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.title = ctk.CTkEntry(master = self, width = 400, placeholder_text = "title")
        self.title.grid(row = 1, column = 0, padx = 20, sticky = "w")

        self.continue_button = ctk.CTkButton(master = self, text = "continue", command = on_click_continue)
        self.continue_button.grid(row = 3, column = 0, pady = 20)

        if invalid_search:
            self.invalid_search_label = ctk.CTkLabel(self, text = "Please provide valid search criteria.", text_color = "red")
            self.invalid_search_label.grid(row = 4, column = 0, padx = 20, pady = (0, 20), sticky = "w")

    def get_title(self):
        return self.title.get()
