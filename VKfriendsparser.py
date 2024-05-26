import json
import vk_api
import configparser
import asyncpg
import asyncio
from time import time
from pydantic import BaseModel, ConfigDict, Field

class Relatives(BaseModel):
    id: int = -1
    type: str = ''
    birth_date: str = ''
    name: str = ''

class Place(BaseModel):
    id: int
    title: str

class Career(BaseModel):
    city_id: int = -1
    country_id: int = -1
    company: str = ''
    group_id: int = -1
    position: str = ''

class University(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: int = -1
    name: str = ''
    faculty_name: str = ''
    chair_name: str = ''
    education_form: str = ''
    education_status: str = ''
    graduation: str = ''
    city: int = -1
    country: int = -1

class School(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    name: str = ''
    type_str: str = ''
    speciality: str = ''
    year_from: str = ''
    year_graduated: str = ''
    year_to: str = ''

class Person(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: int
    first_name: str = ''
    last_name: str = ''
    bdate: str = ''
    photo: str = Field(default='', alias='photo_max_orig')
    city: Place = Place(id = -1, title = '')
    sex: int = 0
    mobile_phone: str = ''
    home_phone: str = ''
    site: str = ''
    home_town: str = ''
    verified: bool = None
    university_name: str = ''
    faculty_name: str = ''
    graduation: str = ''
    education_form: str = ''
    education_status: str = ''
    relatives: list[Relatives] = []
    career: list[Career] = []
    universities: list[University] = []
    schools: list[School] = []
    status: str = ''
    interests: str = ''
    books: str = ''
    tv: str = ''
    quotes: str = ''
    about: str = ''
    games: str = ''
    movies: str = ''
    activities: str = ''
    music: str = ''

def timer_decorator(func):
    def wrapper():
        start_time = time()
        func()
        end_time = time()
        print(f"Время выполнения: {end_time - start_time} секунд")
    return wrapper

def generate_sql_query(tablename: str, columns: tuple) -> str:
    sql = """INSERT INTO """ + tablename + """(id, """
    for index, col in enumerate(columns):
        if index != len(columns)-1:
            sql += col + ', '
        else:
            sql += col + ')\n'
    sql += 'VALUES('
    for i in range(len(columns)):
        sql += "$" + str(i + 1) + ", "
    sql += '$' + str(len(columns) + 1) + ')\n'
    sql += 'ON CONFLICT (id) DO UPDATE \nSET '
    for index, col in enumerate(columns):
        if index != len(columns)-1:
            sql += col + ' = EXCLUDED.' + col + ',\n'
        else:
            sql += col + ' = EXCLUDED.' + col + ';'
    return sql

async def vkfriends_table(friends: list, config: configparser) -> None:
    cols = ('first_name', 'last_name', 'bdate', 'photo', 'city', 'sex', 'mobile_phone', 'home_phone', 'site', 'home_town', 'verified', 'university_name', 'faculty_name', 
            'graduation', 'education_form', 'education_status', 'relatives', 'career', 'universities', 'schools', 'status', 'interests', 'books', 'tv', 'quotes', 
            'about', 'games', 'movies', 'activities', 'music')
    sql = generate_sql_query('VKFriends', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump()
        datadict['city'] = datadict['city']['title']
        if datadict['sex'] == 2:
            datadict['sex'] = 'Мужской'
        elif datadict['sex'] == 1:
            datadict['sex'] = 'Женский'
        else:
            datadict['sex'] = ''
        datadict['relatives'] = json.dumps(datadict['relatives'], ensure_ascii=False)
        datadict['career'] = json.dumps(datadict['career'], ensure_ascii=False)
        datadict['universities'] = json.dumps(datadict['universities'], ensure_ascii=False)
        datadict['schools'] = json.dumps(datadict['schools'], ensure_ascii=False)
        await conn.execute(sql, *datadict.values())
    await conn.close()

async def general_table(friends: list, config: configparser) -> None:
    cols = ('first_name', 'last_name', 'bdate', 'city', 'sex', 'home_town', 'verified')
    sql = generate_sql_query('VKGeneralInfo', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump(include={'id', *cols})
        datadict['city'] = datadict['city']['title']
        if datadict['sex'] == 2:
            datadict['sex'] = 'Мужской'
        elif datadict['sex'] == 1:
            datadict['sex'] = 'Женский'
        else:
            datadict['sex'] = ''
        await conn.execute(sql, *datadict.values())
    await conn.close()

async def contact_table(friends: list, config: configparser) -> None:
    cols = ('first_name', 'last_name', 'mobile_phone', 'home_phone', 'site')
    sql = generate_sql_query('VKContactInfo', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump(include={'id', *cols})
        await conn.execute(sql, *datadict.values())
    await conn.close()

async def education_table(friends: list, config: configparser) -> None:
    cols = ('university_name', 'faculty_name', 'graduation', 'education_form', 'education_status', 'career', 'universities', 'schools')
    sql = generate_sql_query('VKEducationInfo', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump(include={'id', *cols})
        datadict['career'] = json.dumps(datadict['career'], ensure_ascii=False)
        datadict['universities'] = json.dumps(datadict['universities'], ensure_ascii=False)
        datadict['schools'] = json.dumps(datadict['schools'], ensure_ascii=False)
        await conn.execute(sql, *datadict.values())
    await conn.close()

async def about_table(friends: list, config: configparser) -> None:
    cols = ('photo', 'status', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'activities', 'music')
    sql = generate_sql_query('VKAboutInfo', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump(include={'id', *cols})
        await conn.execute(sql, *datadict.values())
    await conn.close()

async def relatives_table(friends: list, config: configparser) -> None:
    cols = ('type', 'birth_date', 'name', 'relation_id')
    sql = generate_sql_query('VKRelativesInfo', cols)
    conn = await asyncpg.connect(user=config["postgresql"]["user"], password=config["postgresql"]["password"],
                                 database=config["postgresql"]["database"], host='localhost')
    print('Connected to the PostgreSQL server.')
    for person in friends:
        data = Person(**person)
        datadict = data.model_dump(include={'id', 'relatives'})
        for relative in datadict['relatives']:
            relative['relation_id'] = datadict['id']
            await conn.execute(sql, *relative.values())
    await conn.close()

@timer_decorator
def main():
    config = configparser.ConfigParser()
    config.read("settings.ini")

    # vk_session = vk_api.VkApi(config["VK"]["username2"], config["VK"]["password"], app_id=6287487)
    # vk_session.auth()
    vk_session = vk_api.VkApi(token=config["VK"]["token"])

    vk = vk_session.get_api()

    fieldsneed = 'activities,about,books,bdate,career,contacts,city,country,education,followers_count,home_town,sex,site,schools,screen_name,status,verified,games,interests,last_seen,maiden_name,military,movies,music,occupation,personal,photo_max_orig,quotes,relation,relatives,tv,universities'
    friends = vk.friends.get(user_id = , fields = fieldsneed)['items']
    # print(vk.users.get(fields = fieldsneed))

    start = time()
    config.read("database.ini")

    async def async_main():
        # await vkfriends_table(friends, config)
        await asyncio.gather(vkfriends_table(friends, config),
            general_table(friends, config))
        await asyncio.gather(relatives_table(friends, config),
            contact_table(friends, config),
            education_table(friends, config),
            about_table(friends, config))
    
    asyncio.run(async_main())

    print('Время записи -', time() - start)

if __name__ == "__main__":
    main()