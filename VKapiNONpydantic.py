import vk_api
import configparser
import psycopg2

def generate_sql_query(columns: tuple) -> str:
    sql = """INSERT INTO VKFriends(id, """
    for index, col in enumerate(columns):
        if index != len(columns)-1:
            sql += col + ', '
        else:
            sql += col + ')\n'
    sql += 'VALUES('
    for _ in range(len(columns)):
        sql += "%s, "
    sql += '%s)\n'
    sql += 'ON CONFLICT (id) DO UPDATE \nSET '
    for index, col in enumerate(columns):
        if index != len(columns)-1:
            sql += col + ' = EXCLUDED.' + col + ',\n'
        else:
            sql += col + ' = EXCLUDED.' + col + ';'
    return sql

def main():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    vk_session = vk_api.VkApi(config["VK"]["username"], config["VK"]["password"], app_id=6287487)
    vk_session.auth()

    vk = vk_session.get_api()

    fieldsneed = 'activities, about, books, bdate, career, common_count, contacts, city, country, education, followers_count, home_town, sex, site, schools, screen_name, status, verified, games, interests, last_seen, maiden_name, military, movies, music, occupation, personal, photo_max_orig, quotes, relation, relatives, tv, universities'
    friends = vk.friends.get(user_id = , fields = fieldsneed)['items']

    # print(vk.friends.get(count = 2, fields = fieldsneed))
    # print(vk.users.get(fields = fieldsneed))
    # print(vk.users.get(user_ids = z['items'][0], fields = fieldsneed))
    # friends = [{'id': 764188140, 'domain': 'id764188140', 'bdate': '12.9.2001', 'city': {'id': 99, 'title': 'Новосибирск'}, 'country': {'id': 1, 'title': ''}, 'timezone': 7.0, 'photo_max_orig': 'https://sun4-20.userapi.com/s/v1/ig2/b0KYLlrD2vyhH4rvx_Iaos_9RNDVymnleKfWAw_tePhvHG-Cxx9Jy9ahbv6TH66TSXl66y1Z5GWoSlfPS48qRVmt.jpg?size=400x400&quality=95&crop=0,0,701,701&ava=1', 'is_friend': 0, 'can_post': 1, 'can_see_all_posts': 1, 'can_see_audio': 1, 'skype': '321xd', 'interests': 'inteterst', 'books': 'book', 'tv': 'show', 'quotes': 'quote', 'about': 'about me', 'games': 'game, game', 'movies': 'movie', 'activities': 'do', 'music': 'music', 'can_write_private_message': 1, 'can_send_friend_request': 1, 'can_be_invited_group': True, 'mobile_phone': '88005553535', 'home_phone': '88005553535', 'site': 'xd.com', 'status': 'About info', 'last_seen': {'platform': 7, 'time': 1713891042}, 'followers_count': 2, 'blacklisted': 0, 
    # 'blacklisted_by_me': 0, 'is_favorite': 0, 'is_hidden_from_feed': 0, 'common_count': 0, 'career': [{'city_id': 99, 'country_id': 1, 'from': 2024, 'group_id': 31426815, 'position': 'Junior Developer', 'until': 2024}], 'military': [{'unit': '20115', 'unit_id': 56, 'country_id': 1, 'from': 2021, 'until': 2025}, {'unit': '234234', 'unit_id': 612, 'country_id': 1, 'from': 1997, 'until': 2003}], 'university': 0, 'university_name': '', 'faculty': 0, 'faculty_name': '', 'graduation': 0, 'home_town': 'Иркутск', 'relation': 1, 'personal': {'alcohol': 2, 'inspired_by': 'Gen Richard, Ben Brook, Don Gibon', 'langs': ['Русский', '日本語', 'English'], 'langs_full': [{'id': 0, 'native_name': 'Русский'}, {'id': 20, 'native_name': '日本語'}, {'id': 3, 'native_name': 'English'}], 'life_main': 1, 'people_main': 1, 'political': 5, 'religion': 'Православие', 'religion_id': 102, 'smoking': 1}, 'universities': [], 'schools': [{'city': 99, 'country': 1, 'id': '285709', 'name': 'Новосибирский областной колледж культуры и искусств (НОККиИ)', 'type': 8, 'type_str': 'Колледж', 'year_from': 2024, 'year_graduated': 2031, 'year_to': 2031, 'speciality': 'specialty'}, {'city': 99, 'country': 1, 'id': '1854153', 'name': 'Специальная (коррекционная) школа № 1', 'year_from': 2024, 'year_graduated': 2031, 
    # 'year_to': 2031, 'speciality': 'specialty1'}], 'relatives': [{'type': 'child', 'birth_date': '31.12.2010', 'id': -679603143, 'name': 'Nameson Secondnameson'}, {'type': 'grandparent', 'id': 216374334}, {'type': 'child', 'birth_date': '01.01.2016', 'id': -406265418, 'name': 'Secondson Secondssonsecondname'}], 'sex': 2, 'screen_name': 'id764188140', 'online': 1, 'verified': 0, 'first_name': 'Илья', 'last_name': 'Шустров', 'can_access_closed': True, 'is_closed': False}]
    collectimportant = ('first_name', 'last_name', 'bdate', 'photo_max_orig')
    collectother = ('mobile_phone', 'home_phone', 'site', 'home_town')
    
    cols = ('first_name', 'last_name', 'bdate', 'photo', 'city', 'sex', 'mobile_phone', 'home_phone', 'site', 'home_town', 'verified')
    sql = generate_sql_query(cols)

    config.read("database.ini")
    try:
        with psycopg2.connect(host = 'localhost', dbname = config["postgresql"]["database"], user = config["postgresql"]["user"], password = config["postgresql"]["password"]) as conn:
            with  conn.cursor() as cur:
                print('Connected to the PostgreSQL server.')
                for person in friends:
                    data = [person['id']]
                    for key in collectimportant:
                        if key in person:
                            data.append(person[key])
                        else:
                            data.append('')
                    if 'city' in person:
                        data.append(person['city']['title'])
                    else:
                        data.append('')
                    if person['sex'] == 2:
                        data.append('Мужской')
                    elif person['sex'] == 1:
                        data.append('Женский')
                    else:
                        data.append('')
                    for key in collectother:
                        if key in person:
                            data.append(person[key])
                        else:
                            data.append('')
                    if 'verified' in person:
                        data.append(str(person['verified']))
                    else:
                        data.append(None)
                    cur.execute(sql, data)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    main()

# print(vk.messages.send(user_id = z['items'][0], random_id = 0, message = 'Проверка кода'))


# print(vk.messages.send(user_id = 367426762, random_id = 0, message = 'Проверка кода'))

# x = vk.messages.getHistory(user_id = 367426762, count = 1)
# text = x.get('items')[0]['text']
# print(x)

"""
{'count': 1, 'items': [{'id': 216374334, 'bdate': '2.12', 'city': {'id': 99, 'title': 'Новосибирск'}, 
'photo_max_orig': 'https://sun4-22.userapi.com/s/v1/ig2/J4kVvob2eMYZmzIy-PX3sVY58offMgCNqJ1PEOOq_H15qhLqGoum6AhD-4E3zH9YS98ALjtZp3qAkxLVgQrO5ByW.jpg?size=400x538&quality=95&crop=188,256,1520,2048&ava=1', 
'interests': '', 'books': '', 'tv': '', 'quotes': '', 'about': '', 'games': '', 'movies': '', 'activities': '', 'music': '', 'mobile_phone': '', 'home_phone': '', 'site': '', 
'status': "Take a picture, it'll last longer", 'last_seen': {'platform': 7, 'time': 1713962856}, 'followers_count': 50, 'common_count': 0, 'career': [], 'military': [], 
'university': 0, 'university_name': '', 'faculty': 0, 'faculty_name': '', 'graduation': 0, 'home_town': 'Aokigahara', 'relation': 3, 
'relation_partner': {'id': 367426762, 'first_name': 'Севиль', 'last_name': 'Алекберова'}, 
'personal': {'alcohol': 0, 'inspired_by': '', 'langs': ['Русский'], 'langs_full': [{'id': 0, 'native_name': 'Русский'}], 'life_main': 0, 'people_main': 0, 'smoking': 0}, 
'universities': [], 'schools': [], 'relatives': [], 'track_code': '9dda8812jWatal5R6SrhWDC7OOv1xb-2DNRwUdlNI2C8v7Jpj0rgDaMMYlLrJOtdBFHdbjOszKIV2Gc_vT58', 'sex': 2, 
'screen_name': 'mapyax', 'verified': 0, 'first_name': 'Андрей', 'last_name': 'Прохоров', 'can_access_closed': True, 'is_closed': False}]}

[{'id': 764188140, 'domain': 'id764188140', 'bdate': '12.9.2001', 'city': {'id': 99, 'title': 'Новосибирск'}, 'country': {'id': 1, 'title': 'Россия'}, 'timezone': 7.0, 'photo_max_orig': 'https://sun4-20.userapi.com/s/v1/ig2/b0KYLlrD2vyhH4rvx_Iaos_9RNDVymnleKfWAw_tePhvHG-Cxx9Jy9ahbv6TH66TSXl66y1Z5GWoSlfPS48qRVmt.jpg?size=400x400&quality=95&crop=0,0,701,701&ava=1', 'is_friend': 0, 'can_post': 1, 'can_see_all_posts': 1, 'can_see_audio': 1, 'skype': '321xd', 'interests': 'inteterst', 'books': 'book', 'tv': 'show', 'quotes': 'quote', 'about': 'about me', 'games': 'game, game', 'movies': 'movie', 'activities': 'do', 'music': 'music', 'can_write_private_message': 1, 'can_send_friend_request': 1, 'can_be_invited_group': True, 'mobile_phone': '88005553535', 'home_phone': '88005553535', 'site': 'xd.com', 'status': 'About info', 'last_seen': {'platform': 7, 'time': 1713891042}, 'followers_count': 2, 'blacklisted': 0, 
'blacklisted_by_me': 0, 'is_favorite': 0, 'is_hidden_from_feed': 0, 'common_count': 0, 'career': [{'city_id': 99, 'country_id': 1, 'from': 2024, 'group_id': 31426815, 'position': 'Junior Developer', 'until': 2024}], 'military': [{'unit': '20115', 'unit_id': 56, 'country_id': 1, 'from': 2021, 'until': 2025}, {'unit': '234234', 'unit_id': 612, 'country_id': 1, 'from': 1997, 'until': 2003}], 'university': 0, 'university_name': '', 'faculty': 0, 'faculty_name': '', 'graduation': 0, 'home_town': 'Иркутск', 'relation': 1, 'personal': {'alcohol': 2, 'inspired_by': 'Gen Richard, Ben Brook, Don Gibon', 'langs': ['Русский', '日本語', 'English'], 'langs_full': [{'id': 0, 'native_name': 'Русский'}, {'id': 20, 'native_name': '日本語'}, {'id': 3, 'native_name': 'English'}], 'life_main': 1, 'people_main': 1, 'political': 5, 'religion': 'Православие', 'religion_id': 102, 'smoking': 1}, 'universities': [], 'schools': [{'city': 99, 'country': 1, 'id': '285709', 'name': 'Новосибирский областной колледж культуры и искусств (НОККиИ)', 'type': 8, 'type_str': 'Колледж', 'year_from': 2024, 'year_graduated': 2031, 'year_to': 2031, 'speciality': 'specialty'}, {'city': 99, 'country': 1, 'id': '1854153', 'name': 'Специальная (коррекционная) школа № 1', 'year_from': 2024, 'year_graduated': 2031, 
'year_to': 2031, 'speciality': 'specialty1'}], 'relatives': [{'type': 'child', 'birth_date': '31.12.2010', 'id': -679603143, 'name': 'Nameson Secondnameson'}, {'type': 'grandparent', 'id': 216374334}, {'type': 'child', 'birth_date': '01.01.2016', 'id': -406265418, 'name': 'Secondson Secondssonsecondname'}], 'sex': 2, 'screen_name': 'id764188140', 'online': 1, 'verified': 0, 'first_name': 'Илья', 'last_name': 'Шустров', 'can_access_closed': True, 'is_closed': False}]

[{'id': 216374334, 'domain': 'mapyax', 'bdate': '2.12', 'city': {'id': 99, 'title': 'Новосибирск'}, 'country': {'id': 1, 'title': 'Россия'}, 'photo_max_orig': 'https://sun4-22.userapi.com/s/v1/ig2/J4kVvob2eMYZmzIy-PX3sVY58offMgCNqJ1PEOOq_H15qhLqGoum6AhD-4E3zH9YS98ALjtZp3qAkxLVgQrO5ByW.jpg?size=400x538&quality=95&crop=188,256,1520,2048&ava=1', 'is_friend': 1, 'can_post': 0, 'can_see_all_posts': 1, 'can_see_audio': 1, 'interests': '', 'books': '', 'tv': '', 'quotes': '', 'about': '', 'games': '', 'movies': '', 'activities': '', 'music': '', 'can_write_private_message': 1, 'can_send_friend_request': 1, 'can_be_invited_group': True, 'mobile_phone': '', 'home_phone': '', 'site': '', 'status': "Take a picture, it'll last longer", 'last_seen': {'platform': 7, 'time': 1713888876}, 'followers_count': 50, 'blacklisted': 0, 'blacklisted_by_me': 0, 'is_favorite': 0, 'is_hidden_from_feed': 0, 'common_count': 0, 'career': [], 'military': [], 'university': 0, 'university_name': '', 'faculty': 0, 'faculty_name': '', 'graduation': 0, 'home_town': 'Aokigahara', 'relation': 3, 'relation_partner': {'id': 367426762, 'first_name': 'Севиль', 'last_name': 'Алекберова'}, 'personal': {'alcohol': 0, 'inspired_by': '', 'langs': ['Русский'], 'langs_full': [{'id': 0, 'native_name': 'Русский'}], 'life_main': 0, 'people_main': 0, 'smoking': 0}, 'universities': [], 'schools': [], 'relatives': [], 'sex': 2, 'screen_name': 'mapyax', 'online': 0, 'verified': 0, 'first_name': 'Андрей', 'last_name': 'Прохоров', 'can_access_closed': True, 'is_closed': False}]
"""