import sqlite3
import json


def search_by_title(title):
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    cursor.execute(f"""SELECT title, country, release_year, listed_in, description FROM netflix
                    WHERE title = '{title}'
                    ORDER BY release_year DESC
                    LIMIT 1
                    """)
    executed_db = cursor.fetchall()
    connection.close()

    if executed_db:
        movie = {
            "title": executed_db[0][0],
            "country": executed_db[0][1],
            "release_year": executed_db[0][2],
            "genre": executed_db[0][3],
            "description": executed_db[0][4]
        }
        return movie
    return None


def search_by_year(start, stop):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    query = f"""SELECT title, release_year FROM netflix
                WHERE type = 'Movie' AND release_year BETWEEN {start} AND {stop}
                ORDER BY release_year
                LIMIT 100
                """
    cur.execute(query)
    response = cur.fetchall()
    con.close()

    if response:
        return json.dumps(response)
    return None


def search_by_rating(rating):
    if rating == "child":
        rating = ("G")
    elif rating == "family":
        rating = ("PG", "PG-13")
    elif rating == "adult":
        rating = ("R", "NC-17")
    else:
        return None

    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    cur.execute(f"""SELECT title, rating, description FROM netflix
                    WHERE rating IN {rating}
                    """)
    response = cur.fetchall()

    if response:
        return json.dumps(response)
    return None


def get_freshest_by_genre(genre):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    request = f"""SELECT title, description FROM netflix
                 WHERE listed_in LIKE '%{genre}%' AND type = 'Movie'
                 ORDER BY release_year DESC
                 LIMIT 10
                 """
    cur.execute(request)

    response = cur.fetchall()

    if response:
        return json.dumps(response)
    return None


def get_close_actors(actor):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    request = f"""SELECT "cast" FROM netflix
                 WHERE "cast" LIKE '%{actor}%'
                 """
    cur.execute(request)
    response = cur.fetchall()

    actors = {}

    for cast in response:
        actors_list = cast[0].split(", ")
        for actor_name in actors_list:
            if actor_name in actors.keys():
                actors[actor_name] = True
            else:
                actors[actor_name] = False

    print(actors)

    close_actors = []
    for actor_name, is_played in actors.items():
        if is_played:
            close_actors.append(actor_name)

    if close_actors:
        return close_actors
    return None


tst = get_close_actors("Rose McIver")
print(tst)
tst = get_close_actors("Ben Lamb")
print(tst)
tst = get_close_actors("Jason Statham")
print(tst)
tst = get_close_actors("Theo Devaney")
print(tst)

