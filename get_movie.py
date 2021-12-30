import requests

class GetMovie:
    def __init__(self, movie_to_search):
        self.movie_search_url = "https://api.themoviedb.org/3/search/movie"
        self.parameters = {
            "api_key": "a4cfa61602a55b61908dae8213acf485",
            "language": "en-US",
            "query": movie_to_search,
            "adult": True
        }
        self.index = 0
        self.movie_list = []
        self.movie_list.clear()
        self.movie_data = requests.get(url=self.movie_search_url, params=self.parameters).json()
        self.add_movies_to_list()
        self.final_movie_list = self.movie_list

    def add_movies_to_list(self):
        for data in self.movie_data["results"]:
            self.movie_list.append(
                {
                    "index_no": self.index,
                    "movie_db_id": data['id'],
                    "title": data["original_title"],
                    "overview": data["overview"],
                    "release_date": data["release_date"],
                    "poster_path": data["poster_path"],
                    "rating": data["vote_average"],
                    "poster_url": f"https://image.tmdb.org/t/p/original{data['poster_path']}"
                }
            )
            self.index = self.index + 1
