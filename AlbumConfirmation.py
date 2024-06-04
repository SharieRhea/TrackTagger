import customtkinter as ctk
from PIL import Image
from io import BytesIO

class AlbumConfirmation(ctk.CTkFrame):
    """Holds the UI to display an album's cover and info for confirmation."""

    def __init__(self, master, title, artist, album_title, album_artist, cover, on_click_yes, on_click_no):
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
            The title of the album.
        album_artist: str
            The artist of the album.
        cover: Image
            The URL for the albun's cover image.
        on_click_yes: Callable[]
            Defines on-click behavior for the yes button.
        on_click_no: Callable[]
            Defines on-click behavior for the no button.
        """
        super().__init__(master)

        # center items horizontally
        self.columnconfigure(index = 0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"Accept the following album for {title} by {artist}?")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.album_sub_frame = ctk.CTkFrame(master = self)
        self.album_sub_frame.grid(row = 1, column = 0, padx = 20, pady = (0, 20), sticky = "ew")

        image = ctk.CTkImage(light_image = Image.open(BytesIO(cover)), size = (150, 150))
        self.cover_image = ctk.CTkLabel(master = self.album_sub_frame, image = image, text = "")
        self.cover_image.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.album_info_label = ctk.CTkLabel(master = self.album_sub_frame, text = f"{album_title} by {album_artist}")
        self.album_info_label.grid(row = 0, column = 1, padx = 20, pady = 20)

        self.button_sub_frame = ctk.CTkFrame(master = self)
        self.button_sub_frame.grid(row = 2, column = 0, padx = 20, pady = (0, 20))

        self.no_button = ctk.CTkButton(master = self.button_sub_frame, text = "no", fg_color = "grey", hover_color = "dark grey", command = on_click_no)
        self.no_button.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.yes_button = ctk.CTkButton(master = self.button_sub_frame, text = "yes", command = on_click_yes)
        self.yes_button.grid(row = 0, column = 1, padx = 20, pady = 20)
