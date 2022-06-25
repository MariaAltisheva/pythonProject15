import json
import sqlite3


def _list_film(result):
    """Функция принимает значения базы данных и выдает структурированный список"""
    list_film = []

    for i in range(len(result)):
        dictionary_film = {}
        dictionary_film["title"] = result[i - 1][0]
        dictionary_film["country"] = result[i - 1][1]
        dictionary_film["release_year"] = result[i - 1][2]
        dictionary_film["genre"] = result[i - 1][3]
        dictionary_film["description"] = result[i - 1][4]
        list_film.append(dictionary_film)
        return list_film

def _list_film_for_rating(result):
    """Функция, которая создает приемлемый список json по рейтингу"""
    new_list = []
    for i in range(len(result)):
        dictionary_film = {}
        dictionary_film["title"] = result[i - 1][0]
        dictionary_film["rating"] = result[i - 1][1]
        dictionary_film["description"] = result[i - 1][2]
        new_list.append(dictionary_film)
    jsonStr = json.dumps(new_list)
    return jsonStr

def request_title(title):
    """Функция получает слово в назавнии фильма и выводит
     информацию о последнем фильме"""
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT `title`, `country`,
                        `release_year`, `listed_in`, `description`
                        FROM netflix 
                        WHERE `title` LIKE '%{title}%'
                        ORDER BY `release_year` DESC 
                        """
    cur.execute(sqlite_query)
    result = cur.fetchall()
    new_result = _list_film(result)[0]

    con.close()
    return new_result

def request_film_by_year(year1, year2):
    """Функция получает диапазон лет и выводит
     информацию о 100 последних фильмах"""
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT `title`,
                        `release_year`
                        FROM netflix 
                        WHERE `release_year` BETWEEN {year1} AND {year2}
                        ORDER BY `release_year` DESC Limit 100
                        """
    cur.execute(sqlite_query)
    result = cur.fetchall()
    new_list = []
    for i in range(len(result)):
        dictionary_film = {}
        dictionary_film["title"] = result[i - 1][0]
        dictionary_film["release_year"] = result[i - 1][1]
        new_list.append(dictionary_film)
    con.close()
    jsonStr = json.dumps(new_list)
    return jsonStr

def search_by_rating(rating):
    if rating == 'children':
        con = sqlite3.connect("netflix.db")
        cur = con.cursor()
        sqlite_query = f"""SELECT `title`,
                            `rating`, `description`
                            FROM netflix 
                            WHERE `rating` LIKE '%G%'
                            LIMIT 100
                            """
        cur.execute(sqlite_query)
        result = cur.fetchall()
        con.close()
        return _list_film_for_rating(result)

    elif rating == 'family':
        con = sqlite3.connect("netflix.db")
        cur = con.cursor()
        sqlite_query = f"""SELECT `title`,
                            `rating`, `description`
                            FROM netflix 
                            WHERE `rating` LIKE '%G%' OR '%PG%' OR '%PG-13%'
                            LIMIT 100
                            """
        cur.execute(sqlite_query)
        result = cur.fetchall()
        con.close()
        return _list_film_for_rating(result)

    elif rating == 'adult':
        con = sqlite3.connect("netflix.db")
        cur = con.cursor()
        sqlite_query = f"""SELECT `title`,
                                    `rating`, `description`
                                    FROM netflix 
                                    WHERE `rating` LIKE '%R%' OR '%NC-17%'
                                    LIMIT 100
                                    """
        cur.execute(sqlite_query)
        result = cur.fetchall()
        con.close()
        return _list_film_for_rating(result)
    else:
        return f'Данные не корректны'

def search_by_genre(genre):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT `title`,
                                    `description`
                                    FROM netflix 
                                    WHERE `listed_in` LIKE '%{genre}%'
                                    ORDER BY `release_year` DESC 
                                    LIMIT 10
                                    """
    cur.execute(sqlite_query)
    result = cur.fetchall()
    new_list = []
    for i in range(len(result)):
        dictionary_film = {}
        dictionary_film["title"] = result[i - 1][0]
        dictionary_film["description"] = result[i - 1][1]
        new_list.append(dictionary_film)
    con.close()
    jsonStr = json.dumps(new_list)
    return jsonStr

