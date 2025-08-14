import customtkinter
from api import Movies


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        # default
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.geometry("350x500")
        self.grid_columnconfigure((0), weight=1)

        self.row_index = 0

        self.switch = customtkinter.CTkSwitch(
            self, text="Dark theme", onvalue='on', offvalue='off', command=self.set_theme)
        self.switch.grid(row=self.row_index, column=0)
        self.row_index += 1

        self.entry = customtkinter.CTkEntry(self, width=140)
        self.entry.grid(row=self.row_index, column=0, padx=20, pady=5)
        self.row_index += 1

        self.button = customtkinter.CTkButton(
            self, text="Search", command=self.button_event, width=70)
        self.button.grid(row=self.row_index, column=0, pady=3)
        self.row_index += 1

        self.title_label = customtkinter.CTkLabel(self, text=None)
        self.release_label = customtkinter.CTkLabel(self, text=None)
        self.overview_label = customtkinter.CTkLabel(
            self, text=None, wraplength=250)
        self.rating_label = customtkinter.CTkLabel(self, text=None)

        for label in [self.title_label, self.release_label, self.overview_label, self.rating_label]:
            label.grid(row=self.row_index, column=0, pady=5)
            self.row_index += 1

    def set_theme(self):
        if self.switch.get() == 'on':
            self.switch.configure(text="Light theme")
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")
        elif self.switch.get() == 'off':
            self.switch.configure(text="Dark theme")
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

    def button_event(self):
        app_api = Movies()
        try:
            movie_name = self.entry.get()
            movie = app_api.search(movie_name)
            first_result = movie[0]

            self.title_label.configure(text=f"Title: {first_result['title']}")
            self.release_label.configure(
                text=f"Release Date: {first_result['release_date']}")
            self.overview_label.configure(
                text=f"Overview: {first_result['overview']}")
            self.rating_label.configure(
                text=f"Rating: {first_result['vote_average']:.2f}")

        except IndexError as e:
            print(f"Error: {e}")
            self.title_label.configure(text="Could not find that movie")
            self.release_label.configure(text="")
            self.overview_label.configure(text="")
            self.rating_label.configure(text="")


if __name__ == "__main__":
    app = App()
    app.mainloop()
