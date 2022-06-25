import sqlite3
import json

def two_actor(actor_1, actor_2):
    """Функция получает двух актеров и выводит список тех, кто играт с ними в паре более двух раз"""
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT `cast` FROM netflix 
                        WHERE `cast` LIKE '%{actor_1}%' OR '%{actor_2}%'
                        """
    cur.execute(sqlite_query)
    result = cur.fetchall()
    con.close()
    list_of_actors = []
    for i in result:
        for y in i:
            list_of_actors.append(y)
    new_list = "".join(list_of_actors)
    finish_list = new_list.split(', ')
    super_finish_list = []
    for i in finish_list:
        if finish_list.count(i) > 2 and i != actor_2 and i != actor_1:
            super_finish_list.append(i)

    return super_finish_list

def for_step_6(type, year, genre):
    """С помощью данной функции можно задать параметры тип, год и жарнр, а получить список картин с описаниями"""
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = f"""SELECT `title`, `description` FROM netflix 
                            WHERE `type` LIKE '%{type}%' AND `release_year` LIKE '%{year}%'AND `listed_in` LIKE '%{genre}%'
                            """
    cur.execute(sqlite_query)
    result = cur.fetchall()
    con.close()
    new_list = []
    for i in range(len(result)):
        dictionary_film = {}
        dictionary_film["title"] = result[i - 1][0]
        dictionary_film["description"] = result[i - 1][1]
        new_list.append(dictionary_film)
    con.close()
    jsonStr = json.dumps(new_list)
    return jsonStr


print('Список актеров, которые играли более 2-х раз с Ben Lamb и Rose Mclver')
print(two_actor('Ben Lamb', 'Rose Mclver'))

print('\nСписок актеров, которые играли более 2-х раз с Jack Blac и Dustin Hoffman')
print(two_actor('Jack Black', 'Dustin Hoffman'))

print('\nСписок драмм, которые были сняты в 2005 году')
print(for_step_6('movie', '2005', 'dramas'))
