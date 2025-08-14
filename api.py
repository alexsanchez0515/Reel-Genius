import requests
import random
from PIL import Image
from io import BytesIO

# const of user token and api url
API_URL = "https://api.themoviedb.org/3/authentication"
HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMzIyOWZiYmE3YzNkZDlkZmI1YzA0NzA3ZmYxMjUwNyIsIm5iZiI6MTc1NTE3Mzk4Ny40Miwic3ViIjoiNjg5ZGQ0NjNkN2UxMjU2YjQwYzcwYWFkIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.OXfouADxFlXHaLV6y7KQ7kF15pNzkpZTEHl8nag3L-Q"
}

# class Movies to handle api token confirmation, popular movies


class Movies:
    def __init__(self):
        self.confirm_api = requests.get(url=API_URL, headers=HEADERS)
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMzIyOWZiYmE3YzNkZDlkZmI1YzA0NzA3ZmYxMjUwNyIsIm5iZiI6MTc1NTE3Mzk4Ny40Miwic3ViIjoiNjg5ZGQ0NjNkN2UxMjU2YjQwYzcwYWFkIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.OXfouADxFlXHaLV6y7KQ7kF15pNzkpZTEHl8nag3L-Q"
        }
        self.movies = []
        self.actors = []
    # ***FUNCTIONS BELOW ARE FOR FUTURE TRIVIA GAME IMPLEMENTATION***
    # confirm connection to api with token

    def confirm(self):
        return self.confirm_api.json()

    # return a list of popular movies
    def popular(self):
        url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

        response = requests.get(url=url, headers=self.headers)
        return response.json() if response.status_code == 200 else print("Error:", response.status_code, response.text)
    # return a list of the most popular movies for given pages

    def top_rated(self):
        # 20 per page, 10 pages, 200 movies
        for page in range(1, 51):
            url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.movies.extend(data["results"])
            else:
                print("Error:", response.status_code, response.text)

    # actor information for later implementation
    # uses custom_score to attempt to get popular actors of all time
    def get_actors(self, pages, threshold, vote_weight, pop_weight):
        for page in range(1, pages + 1):
            url = f"https://api.themoviedb.org/3/person/popular?&page={page}"
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                print("Error")
                continue

            data = response.json()

            for actor in data["results"]:

                if actor.get("known_for_department") != "Acting":
                    continue

                known_for = actor.get("known_for", [])
                vote_avgs = [item.get("vote_average", 0) for item in known_for if item.get(
                    "vote_average") is not None]

                if vote_avgs:
                    avg_vote = round(sum(vote_avgs) /
                                     len(vote_avgs), ndigits=2)
                else:
                    avg_vote = 0

                tmdb_pop = actor.get("popularity", 0)
                custom_score = round(
                    vote_weight * avg_vote + pop_weight * tmdb_pop, 2)

                if custom_score >= threshold:
                    actor_entry = {
                        "name": actor["name"],
                        "custom_score": custom_score,
                        "known_for": [item["title"] if item["media_type"] == "movie" else item["name"] for item in known_for]
                    }
                    self.actors.append(actor_entry)

    # movie trivia for later implementation
    def trivia_game(self):
        '''while True:
            movie_field = random.choice(list(random_movie.keys()))
            print(movie_field.title())
            print(random_movie[movie_field])

            choice = input(
                "Guess the movie title, get another hint (any key), or exit ('0')? >> ")

            if (choice == "0"):
                break
            if (choice.lower() == random_movie["title"].lower()):
                print(f"That's right, the film is {random_movie['title']}")

            random_movie.pop(movie_field)'''
    # ***FUNCTIONS ABOVE ARE FOR FUTURE TRIVIA GAME IMPLEMENTATION***
    # ***FUNCTIONS BELOW ARE FOR MOVIE RECC IMPLEMENTATION***

    def search(self, name: str):
        url = f"https://api.themoviedb.org/3/search/movie?query={name}"
        response = requests.get(url=url, headers=self.headers)
        return response.json()["results"]

    def get_img(self, movie):
        url = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
        response = requests.get(url=url)
        return Image.open(BytesIO(response.content))


if __name__ == "__main__":
    api = Movies()
    # COMMENTS BELOW ARE FOR TRIVIA FUTURE IMPLEMENTATION
    '''
    print("Loading actors...")
    api.get_actors(pages=200, threshold=7.0, pop_weight=0.3, vote_weight=0.7)
    actors = api.actors
    print("Loading movies...")
    api.top_rated()
    movies = api.movies

    for movie in movies:
        print(movie["title"])
    '''
