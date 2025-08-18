import customtkinter
from api import Movies
from PIL import Image
import bcrypt


class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)


class MovieFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)

# later implementation for seperate single movie frame after selecting movie from results


class RateFrame(customtkinter.CTkFrame):
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
        self.y = 850
        self.title("Reel Genius")
        # self.geometry(
        # f"{self.x}x{self.y}+{self.winfo_screenwidth()-self.x//2}+{self.winfo_screenheight()-self.y//2}")
        self.geometry(f"{self.x}x{self.y}")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.control_frame = ControlFrame(self, width=300, height=100)
        self.control_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.movies_frame = MovieFrame(self,  width=300, height=600)
        self.movies_frame.grid(row=1, column=0, padx=20,
                               pady=20, sticky="nsew")
        self.rate_frame = RateFrame(self, width=300, height=100)
        self.rate_frame.grid(row=2, column=0, padx=20,
                             pady=20, sticky="nsew")
        self.login_frame = LoginFrame(self, width=300, height=100)
        self.login_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

        widgets = [
            customtkinter.CTkSwitch(
                self.control_frame, text="Dark theme", onvalue='on', offvalue='off', command=self.set_theme),
            customtkinter.CTkEntry(
                self.control_frame, width=140, placeholder_text="Film title"),
            customtkinter.CTkButton(
                self.control_frame, text="Search", command=self.search_movies, width=70),
            customtkinter.CTkLabel(
                self.movies_frame, text=None, image=None),
            customtkinter.CTkLabel(
                self.movies_frame, text=None),
            customtkinter.CTkLabel(
                self.movies_frame, text=None),
            customtkinter.CTkLabel(
                self.movies_frame, text=None, wraplength=250),
            customtkinter.CTkLabel(
                self.movies_frame, text=None),
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

    def search_movies(self) -> None:
        app_api = Movies()
        movie_name = self.entry.get()
        results = app_api.search(movie_name)
        movie_list = results[:5]

        for widget in self.movies_frame.winfo_children():
            widget.destroy()

        for index, movie in enumerate(movie_list):
            movie_frame = customtkinter.CTkFrame(self.movies_frame)
            movie_frame.grid(row=index, column=0, padx=10,
                             pady=10, sticky="ew")
            movie_id = movie['id']

            poster_img = customtkinter.CTkImage(
                dark_image=app_api.get_img(movie=movie),
                light_image=app_api.get_img(movie=movie),
                size=(133, 200)
            )

            poster_label = customtkinter.CTkLabel(
                movie_frame, image=poster_img, text="")
            poster_label.image = poster_img
            poster_label.grid(row=0, column=0, rowspan=4, padx=10)

            # Title
            title_label = customtkinter.CTkLabel(
                movie_frame, text=f"Title: {movie['title']}")
            title_label.grid(row=0, column=1, sticky="w")

            # Release date
            release_label = customtkinter.CTkLabel(
                movie_frame, text=f"Release: {movie['release_date']}")
            release_label.grid(row=1, column=1, sticky="w")

            # Overview
            overview_label = customtkinter.CTkLabel(
                movie_frame, text=f"Overview: {movie['overview'][:150]}...", wraplength=250
            )
            overview_label.grid(row=2, column=1, sticky="w")

            # Rating
            rating_label = customtkinter.CTkLabel(
                movie_frame, text=f"Rating: {movie['vote_average']:.1f}")
            rating_label.grid(row=3, column=1, sticky="w")

            select_button = customtkinter.CTkButton(
                master=movie_frame, text=f"Select", command=lambda m_id=movie_id: self.select_movie(id=m_id, frame=self.movies_frame), width=70)
            select_button.grid(row=4, column=1, sticky="nsew")

    def select_movie(self, id, frame):
        print(f"Movie selected: {id}")
        app_api = Movies()
        movie = app_api.find_by_id(id)

        for widget in frame.winfo_children():
            widget.destroy()

        frame._parent_canvas.yview_moveto(0)

        movie_frame = customtkinter.CTkFrame(frame)
        movie_frame.grid(row=0, column=0, padx=10,
                         pady=10, sticky="ew")

        poster_img = customtkinter.CTkImage(
            dark_image=app_api.get_img(movie=movie),
            light_image=app_api.get_img(movie=movie),
            size=(133, 200)
        )

        poster_label = customtkinter.CTkLabel(
            movie_frame, image=poster_img, text="")
        poster_label.image = poster_img
        poster_label.grid(row=0, column=0, rowspan=4, padx=10)

        # Title
        title_label = customtkinter.CTkLabel(
            movie_frame, text=f"Title: {movie['title']}")
        title_label.grid(row=0, column=1, sticky="w")

        # Release date
        release_label = customtkinter.CTkLabel(
            movie_frame, text=f"Release: {movie['release_date']}")
        release_label.grid(row=1, column=1, sticky="w")

        # Overview
        overview_label = customtkinter.CTkLabel(
            movie_frame, text=f"Overview: {movie['overview'][:150]}...", wraplength=250
        )
        overview_label.grid(row=2, column=1, sticky="w")

        # Rating
        rating_label = customtkinter.CTkLabel(
            movie_frame, text=f"Rating: {movie['vote_average']:.1f}")
        rating_label.grid(row=3, column=1, sticky="w")

        # Sliders
        slider_label = customtkinter.CTkLabel(self.rate_frame, text=None)
        slider_label.grid(row=0, column=0, sticky="nsew")
        slider = customtkinter.CTkSlider(self.rate_frame, from_=0, to=10, number_of_steps=100,
                                         width=180, command=lambda value: self.update_slabel(value, slider_label))
        slider.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        slider_button = customtkinter.CTkButton(
            self.rate_frame, text="Rate", command=lambda: self.rate_movie(slider), width=90)
        slider_button.grid(row=2, column=0, padx=5, pady=5)

    def rate_movie(self, slider) -> None:
        print(f"Movie rated: {slider.get()}")

    def update_slabel(self, value, label):
        label.configure(text=f"{value:.1f}")

    def login(self) -> None:
        print("Login pressed")
        username = self.username_entry.get()
        password = self.password_entry.get()


if __name__ == "__main__":
    app = App()
    app.mainloop()
