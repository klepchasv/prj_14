from flask import Flask, request
from search_fnc import search_by_title, search_by_year, search_by_rating, get_freshest_by_genre, get_close_actors, get_film_by_descr


app = Flask(__name__)


@app.route("/movie/<title>")
def find_movie(title):
    movie = search_by_title(title)
    if movie:
        return movie
    return "Film not found", 404


@app.route("/movie/<int:year_start>/<int:year_stop>")
def find_by_year(year_start, year_stop):
    movies = search_by_year(year_start, year_stop)
    if movies:
        return movies
    return "Movies not found", 404


@app.route("/rating/<rating>")
def find_by_rating(rating):
    movies = search_by_rating(rating)
    if movies:
        return movies
    return "Films not found", 404


@app.route("/genre/<genre>")
def find_by_genre(genre):
    movies = get_freshest_by_genre(genre)

    if movies:
        return movies
    return "Movies not found", 404


@app.route("/actors/<actor>")
def find_close_actors(actor):
    close_actors = get_close_actors(actor)

    if close_actors:
        close_actors = ", ".join(close_actors)
        return close_actors
    return "No such actors", 404


@app.route("/movie/<film_type>/<int:release_year>/<genre>")
def find_movie_by_descr(film_type, release_year, genre):
    films = get_film_by_descr(film_type, release_year, genre)

    if films:
        return films
    return "No such movies", 404
    

if __name__ == "__main__":
    app.run(port=8000, debug=True)
