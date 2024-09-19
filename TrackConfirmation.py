import customtkinter as ctk

class TrackConfirmation(ctk.CTkFrame):
    """Holds the UI to display a confirmation dialog for a given track."""

    def __init__(self, master, title, artist, playcount, on_click_yes, on_click_no):
        """
        Initializes UI components.

        Parameters
        ----------
        master: CTk | CTkFrame
            Parent container of this frame.
        title: str
            The title of the track.
        artist: str
            The artist of the track.
        playcount: int
            The number of plays for this song. -1 indicates manual entry (not from last.fm).
        on_click_yes: Callable[]
            Defines on-click behavior for accepting the track.
        on_click_no: Callable[]
            Define on-click behavior for denying the track.
        """
        super().__init__(master)
        
        # center items horizontally
        self.grid_columnconfigure(0, weight = 1)

        if playcount == -1:
            self.message_label = ctk.CTkLabel(master = self, text = f"Accept existing title and artist {title} by {artist}?")
        else:
            self.message_label = ctk.CTkLabel(master = self, text = f"Accept track {title} by {artist} with {playcount} plays?")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.sub_frame = ctk.CTkFrame(self)
        self.sub_frame.grid(row = 1, column = 0, padx = 20, pady = (0, 20))

        self.no_button = ctk.CTkButton(master = self.sub_frame, text = "no", fg_color = "grey", hover_color = "dark grey", command = on_click_no)
        self.no_button.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.yes_button = ctk.CTkButton(master = self.sub_frame, text = "yes", command = on_click_yes)
        self.yes_button.grid(row = 0, column = 1, padx = 20, pady = 20)
