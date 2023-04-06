from models.movie import Movie as MovieModel

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie(self, movie_id):
        movie = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        return movie
    
    def get_movies_by_category(self, category, year=None):
        movies = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movies
    
    def get_movie_by_category(self, category, year=None):
        movie = self.db.query(MovieModel).filter(MovieModel.category == category).first()
        return movie
    
    def create_movie(self, movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()

    def valid_movie(self, movie_id):
        result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        return result
    
    def update_movie(self, result, movie):
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        self.db.commit()
    
    def delete_movie(self, movie):
        self.db.delete(movie)
        self.db.commit()