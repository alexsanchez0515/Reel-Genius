import customtkinter
from api import Movies
from PIL import Image

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)


class MovieFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)

class ControlFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.x = 500
        self.y = 800
        self.title("Reel Genius")
        self.geometry(
            f"{self.x}x{self.y}+{self.winfo_screenwidth()-self.x//2}+{self.winfo_screenheight()-self.y//2}")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.control_frame = ControlFrame(self, width=300, height=100)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_ = MovieFrame(self,  width=300, height=600)
        self.frame_.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.login_frame = LoginFrame(self, width=300, height=100)
        self.login_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        widgets = [
            customtkinter.CTkSwitch(
                self.control_frame, text="Dark theme", onvalue='on', offvalue='off', command=self.set_theme),
            customtkinter.CTkEntry(
                self.control_frame, width=140, placeholder_text="Film title"),
            customtkinter.CTkButton(
                self.control_frame, text="Search", command=self.button_event, width=70),
            customtkinter.CTkLabel(
                self.frame_, text=None, image=None),
            customtkinter.CTkLabel(
                self.frame_, text=None),
            customtkinter.CTkLabel(
                self.frame_, text=None),
            customtkinter.CTkLabel(
                self.frame_, text=None, wraplength=250),
            customtkinter.CTkLabel(
                self.frame_, text=None),
            customtkinter.CTkSlider(
                self.frame_, from_=0, to=10, command=self.slider_event, number_of_steps=100),
            customtkinter.CTkLabel(
                self.frame_, text=None),
            customtkinter.CTkButton(
                self.frame_, text="Rate", command=self.rate_movie, width=70),
            customtkinter.CTkEntry(
                self.login_frame, placeholder_text="Username", width=140),
            customtkinter.CTkEntry(
                self.login_frame, placeholder_text="Password", width=140, show="*"),
            customtkinter.CTkButton(
                self.login_frame, text="Login", command=self.login, width=70),
            customtkinter.CTkCheckBox(
                self.login_frame, text="Remember me", command=None)
        ]

        (
            self.switch,
            self.entry,
            self.button_search,
            self.poster_label,
            self.title_label,
            self.release_label,
            self.overview_label,
            self.rating_label,
            self.slider,
            self.slider_label,
            self.button_rate,
            self.username_entry,
            self.password_entry,
            self.button_login,
            self.remember_check
        ) = widgets

        for widget in widgets:
            if isinstance(widget, customtkinter.CTkButton):
                widget.grid(sticky="", pady=5, padx=5)
            elif isinstance(widget, customtkinter.CTkEntry):
                widget.grid(sticky="", pady=5, padx=5)
            elif isinstance(widget, customtkinter.CTkSlider):
                widget.grid(sticky="", pady=5, padx=5)
            elif isinstance(widget, customtkinter.CTkCheckBox):
                widget.grid(sticky="", pady=5, padx=5)
            elif isinstance(widget, customtkinter.CTkSwitch):
                widget.grid(sticky="", pady=5, padx=5)
            else:
                widget.grid(sticky="ew", pady=5, padx=5)

    def set_theme(self) -> None:
        if self.switch.get() == 'on':
            self.switch.configure(text="Light theme")
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")
        elif self.switch.get() == 'off':
            self.switch.configure(text="Dark theme")
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

    def button_event(self) -> None:
        app_api = Movies()
        movie_name = self.entry.get()
        results = app_api.search(movie_name)

        for widget in self.frame_.winfo_children():
            widget.destroy()

        for index, movie in enumerate(results[:8]):
            movie_frame = customtkinter.CTkFrame(self.frame_)
            movie_frame.grid(row=index, column=0, padx=10, pady=10, sticky="ew")

            poster_img = customtkinter.CTkImage(
                dark_image=app_api.get_img(movie=movie),
                light_image=app_api.get_img(movie=movie),
                size=(100, 150)
            )

            poster_label = customtkinter.CTkLabel(movie_frame, image=poster_img, text="")
            poster_label.image = poster_img
            poster_label.grid(row=0, column=0, rowspan=4, padx=10)

            # Title
            title_label = customtkinter.CTkLabel(movie_frame, text=f"Title: {movie['title']}")
            title_label.grid(row=0, column=1, sticky="w")

            # Release date
            release_label = customtkinter.CTkLabel(movie_frame, text=f"Release: {movie['release_date']}")
            release_label.grid(row=1, column=1, sticky="w")

            # Overview
            overview_label = customtkinter.CTkLabel(
                movie_frame, text=f"Overview: {movie['overview'][:150]}...", wraplength=300
            )
            overview_label.grid(row=2, column=1, sticky="w")

            # Rating
            rating_label = customtkinter.CTkLabel(movie_frame, text=f"Rating: {movie['vote_average']:.2f}")
            rating_label.grid(row=3, column=1, sticky="w")

        '''
        try:
            movie_name = self.entry.get()
            movie = app_api.search(movie_name)
            first_result = movie[0]

            poster_img = customtkinter.CTkImage(
                dark_image=app_api.get_img(first_result),
                light_image=app_api.get_img(first_result),
                size=(200, 300)
            )

            self.slider_label.configure(text=self.slider._value)
            self.poster_label.configure(image=poster_img)
            self.poster_label.image = poster_img
            self.title_label.configure(text=f"Title: {first_result['title']}")
            self.release_label.configure(
                text=f"Release Date: {first_result['release_date']}")
            self.overview_label.configure(
                text=f"Overview: {first_result['overview']}")
            self.rating_label.configure(
                text=f"Rating: {first_result['vote_average']:.2f}")

        except IndexError as e:
            print(f"Error: {e}")
            # positioning issue when image disappears
            self.slider.set(5.0)
            self.poster_label.configure(image=None)
            self.poster_label.image = None
            self.title_label.configure(text="Could not find that movie")
            self.release_label.configure(text="")
            self.overview_label.configure(text="")
            self.rating_label.configure(text="")
        '''

    def slider_event(self, value) -> None:
        self.slider_label.configure(text=f"{value:.1f}")
        ...

    def rate_movie(self) -> None:
        print(f"Movie rated: {self.slider_label._text}")

    def login(self) -> None:
        print("Login pressed")
        print(f"Username: {self.username_entry.get()}")
        print(f"Password: {self.password_entry.get()}")




if __name__ == "__main__":
    app = App()
    app.mainloop()
