
from flask import Flask


from utils import request_title, request_film_by_year, search_by_rating, search_by_genre

app = Flask(__name__)

@app.route('/')
def index():
    """Стартовая страничка"""
    return f"Привет"

@app.route('/movie/<title>')
def page_movies(title):
    """Осуществляет поиск по названию фильма"""
    return request_title(title)

@app.route('/movie/<year1>/to/<year2>')
def page_movies_year(year1, year2):
    """Выводит фильмы в данном диапазоне"""
    return request_film_by_year(year1, year2)

@app.route('/rating/<rating>')
def page_rating(rating):
    """Ищет фильмы для таких категорий, как children, family, adult"""
    return search_by_rating(rating)

@app.route('/genre/<genre>')
def page_genre(genre):
    """Ищет новые фильмы по жанру"""
    return search_by_genre(genre)


if __name__ == '__main__':
    app.run(debug=False)
