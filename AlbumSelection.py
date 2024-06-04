import customtkinter as ctk
import tkinter
import requests
from PIL import Image
from io import BytesIO

class AlbumSelection(ctk.CTkFrame):
    """Holds the UI for selecting one album out of multiple choices."""

    def __init__(self, master, title, artist, albums, on_click_continue, on_click_back):
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
        albums: List[dict]
            The albums to select from.
        on_click_continue: Callable[]
            Defines on-click behavior for the continue button.
        on_click_back: Callable[]
            Defines on-click behavior for the back button.
        """
        super().__init__(master)

        # center items horizontally
        self.columnconfigure(index = 0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"The current track is {title} by {artist}. Please choose an album or search again.")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.sub_frame = ctk.CTkFrame(self)
        self.sub_frame.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = "ew")

        # show at most 5 results
        results_count = 5
        if len(albums) < 5:
                results_count = len(albums)

        # choose first album by default
        self.album_index = tkinter.IntVar(value = 0)

        row_counter = 0
        for i in range(results_count):
            radio_button = ctk.CTkRadioButton(self.sub_frame, text = f"{albums[i]["name"]} by {albums[i]["artist"]}", variable = self.album_index, value = i)

            # grab and display album cover
            cover_url = albums[i]["image"][-1]["#text"]
            if cover_url == "":
                continue
            response = requests.get(albums[i]["image"][-1]["#text"])
            cover = Image.open(BytesIO(response.content))
            image = ctk.CTkImage(light_image = cover, size = (100, 100))
            cover_image = ctk.CTkLabel(master = self.sub_frame, image = image, text = "")

            cover_image.grid(row = row_counter, column = 0, padx = 20, pady = 5)
            radio_button.grid(row = row_counter, column = 1, padx = 20, pady = 5, sticky = "w")
            row_counter = row_counter + 1

        self.button_sub_frame = ctk.CTkFrame(self)
        self.button_sub_frame.grid(row = 2, column = 0, padx = 20, pady = (0, 20))

        self.back_button = ctk.CTkButton(master = self.button_sub_frame, text = "back", fg_color = "grey", hover_color = "dark grey", command = on_click_back)
        self.back_button.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.continue_button = ctk.CTkButton(master = self.button_sub_frame, text = "continue", command = on_click_continue)
        self.continue_button.grid(row = 0, column = 1, padx = 20, pady = 20)

    def get_album_index(self):
        return self.album_index.get()
