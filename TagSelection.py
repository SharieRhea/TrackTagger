import customtkinter as ctk
import tkinter

class TagSelection(ctk.CTkFrame):
    """Holds the UI to display the tag selection dialog."""

    def __init__(self, master, title, artist, tags, allowed, denied, on_click_continue):
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
        tags: List[str]
            List of tags for this track from last.fm.
        allowed: List[str]
            List of user-provided tags to automatically accept.
        denied: List[str]
            List of user-provided tags to automatically deny.
        on_click_continue: Callable[]
            Defines on-click behavior for the continue button.
        """
        super().__init__(master)

        # center items horizontally
        self.columnconfigure(index = 0, weight = 1)

        self.message_label = ctk.CTkLabel(master = self, text = f"Select tags for {title} by {artist}.")
        self.message_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")

        self.sub_frame = ctk.CTkFrame(self)
        self.sub_frame.grid(row = 1, column = 0, padx = 20, pady = (0, 20), sticky = "ew")

        self.checkboxes = []
        for tag in tags:
            if tag in denied:
                state = tkinter.DISABLED
            else:
                state = tkinter.NORMAL

            checkbox = ctk.CTkCheckBox(master = self.sub_frame, text = tag, state = state)

            # denied tags take precedence, should not be disabled and selected
            if state is not tkinter.DISABLED and tag in allowed:
                checkbox.select()
            self.checkboxes.append(checkbox)

        row_counter = 0
        for box in self.checkboxes:
            box.grid(row = row_counter, column = 0, padx = 20, pady = 5, sticky = "w")
            row_counter = row_counter + 1

        self.continue_button = ctk.CTkButton(master = self, text = "continue", command = on_click_continue)
        self.continue_button.grid(row = 2, column = 0, padx = 20, pady = 20)

    def get_selected_tags(self):
        tags = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                tags.append(checkbox.cget("text"))
        return tags

