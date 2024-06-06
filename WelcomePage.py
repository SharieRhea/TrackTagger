import customtkinter as ctk

class WelcomePage(ctk.CTkFrame):
    """ Holds the UI for the opening dialog of track_tagger. Text entries for directory path, allowed tags, and denied tags. """

    def __init__(self, master, on_click_continue, invalid_directory = False):
        """ 
        Initializes UI components.
        
        Parameters
        ----------
        master: CTk | CTkFrame
            Parent container of this frame.
        on_click_continue: Callable[]
            Defines on-click behavior for the continue button.
        invalid_directory: boolean
            True denotes that the provided directory was invalid and triggers an error message.
        """
        super().__init__(master)
        
        # center items horizontally
        self.grid_columnconfigure(0, weight = 1)

        self.welcome_label = ctk.CTkLabel(master = self, text = "Thanks for using track_tragger!", font = ("", 20))
        self.welcome_label.grid(row = 0, column = 0, padx = 20, pady = (20, 5))

        self.api_key_reminder_label = ctk.CTkLabel(master = self, text = "Remember to place your last.fm API key in a .env file.")
        self.api_key_reminder_label.grid(row = 1, column = 0, padx = 20)

        self.directory_path_label = ctk.CTkLabel(master = self, text = "Please provide the path to the directory containing the .mp3 files you wish to process:")
        self.directory_path_label.grid(row = 2, column = 0, padx = 20, pady = (20, 5), sticky = "w")

        self.directory_path = ctk.CTkEntry(master = self, width = 600, placeholder_text = "path/to/directory/")
        self.directory_path.grid(row = 3, column = 0, padx = 20, sticky = "w")

        self.allowed_tags_label = ctk.CTkLabel(master = self, text = "If desired, provide a comma-separated list of tags to auto-accept:")
        self.allowed_tags_label.grid(row = 4, column = 0, padx = 20, pady = (40, 5), stick = "w")

        self.allowed_tags = ctk.CTkEntry(master = self, width = 400, placeholder_text = "pop, rock, alternative")
        self.allowed_tags.grid(row = 5, column = 0, padx = 20, sticky = "w")

        self.denied_tags_label = ctk.CTkLabel(master = self, text = "If desired, provide a comma-separated list of tags to auto-deny:")
        self.denied_tags_label.grid(row = 6, column = 0, padx = 20, pady = (10, 5), sticky = "w")

        self.denied_tags = ctk.CTkEntry(master = self, width = 400, placeholder_text = "favorite, 2010s")
        self.denied_tags.grid(row = 7, column = 0, padx = 20, sticky = "w")

        self.button = ctk.CTkButton(master = self, text = "continue", command = on_click_continue)
        self.button.grid(row = 8, column = 0, padx = 20, pady = 20)

        if invalid_directory:
            self.invalid_directory_label = ctk.CTkLabel(self, text = "Please provide a valid directory path.", text_color = "red")
            self.invalid_directory_label.grid(row = 9, column = 0, padx = 20, pady = (0, 20), sticky = "w")

    def get_directory_path(self):
        return self.directory_path.get()

    def get_allowed_tags(self):
        return self.allowed_tags.get()

    def get_denied_tags(self):
        return self.denied_tags.get()
