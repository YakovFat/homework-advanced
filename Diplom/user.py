import vk
import re
import sys
import time
import json
import copy
from db_mongo import write_to_database
from json_file import json_vkinder
from operator import itemgetter
from datetime import datetime
from config_pass import *

print('Пожалуйста, введите логин и пароль: ')
print('Логин: ')
LOGIN = input()
print('Пароль: ')
PASSWORD = input()
session = vk.AuthSession(app_id=APP_ID, user_login=LOGIN,
                         user_password=PASSWORD, scope='groups')
api = vk.API(session)

FIELDS = 'bdate, sex, city, interests, books, games, movies, music, ' \
         'common_count, relation'


class User:
    def __init__(self, user_id):
        try:
            self.user_id = api.users.get(user_ids=user_id, v='5.92',
                                         fields=FIELDS)
        except KeyError:
            sys.exit('Данного пользователя не существует')

    def city_user(self):
        try:
            return self.user_id[0]['city']['id']
        except KeyError:
            print('Недостаточно данных, пожалуйста, введите двухбуквенный '
                  'код вашей страны(RU,UA,BY):')
            country = input()
            country = api.database.getCountries(v='5.92', code=country, count=1)
            country = country["items"][0]['id']
            print('Пожалуйста, введите ваш город:')
            city = input()
            city = api.database.getCities(v='5.92', country_id=country, q=city,
                                          count=1)
            return city['items'][0]['id']

    def sex_user(self):
        try:
            sex_user = self.user_id[0]['sex']
            if sex_user == 2:
                return 1
            elif sex_user == 1:
                return 2
        except KeyError:
            print('Недостаточно данных, пожалуйста, укажите ваш пол (1 — '
                  'женщина, 2 — мужчина:')
            sex = input()
            if sex == 2:
                return 1
            elif sex == 1:
                return 2

    def age_user(self):
        date_now = datetime.now()
        try:
            if len(self.user_id[0]['bdate']) > 6:
                date_user = datetime.strptime(self.user_id[0]['bdate'],
                                              '%d.%m.%Y')
                age_user = date_now - date_user
                age_user = int(age_user.days / 365)
                return age_user
            else:
                print('Недостаточно данных, пожалуйста, укажите свой возраст:')
                age_user = int(input())
                return age_user
        except KeyError:
            print('Недостаточно данных, пожалуйста, укажите свой возраст:')
            age_user = int(input())
            return age_user

    def user_search(self):
        age = User.age_user(self)
        search = api.users.search(city=User.city_user(self),
                                  sex=User.sex_user(self),
                                  age_from=age - 5,
                                  age_to=age + 5, v='5.92',
                                  fields=FIELDS, count=100, status=6)
        search_copy = copy.copy(search)
        try:
            with open("Vkinder v2.0.json", "r") as data_file:
                data = json.load(data_file)
                if str(self.user_id[0]['id']) in data['user']:
                    for us in data['result']:
                        for i in search_copy['items']:
                            if str(i['id']) in us['profile']:
                                search['items'].remove(i)
        except FileNotFoundError:
            pass
        return search

    def analysis_interests(self):
        info_user = self.user_id[0]
        search = User.user_search(self)['items']
        count = 0
        interests = info_user.setdefault('interests', '').lower().split(', ')
        if interests[0] == '':
            print('Укажите свои интересы: ')
            interests = input().lower().split(
                ', ')
        music = info_user.setdefault('music', '').lower().split(', ')
        if music[0] == '':
            print('Укажите любимую музыку: ')
            music = input().lower().split(
                ', ')
        movies = info_user.setdefault('movies', '').lower().split(', ')
        if movies[0] == '':
            print('Укажите любимые фильмы: ')
            movies = input().lower().split(
                ', ')
        books = info_user.setdefault('books', '').lower().split(', ')
        if books[0] == '':
            print('Укажите любимык книги: ')
            books = input().lower().split(
                ', ')
        games = info_user.setdefault('games', '').lower().split(', ')
        if games[0] == '':
            print('Укажите любимые игры: ')
            games = input().lower().split(
                ', ')
        list_interests = [(interests, 'interests'), (music, 'music'),
                          (movies, 'movies'), (books, 'books'),
                          (games, 'games')]
        for person in search:
            for i in list_interests:
                for string in i[0]:
                    try:
                        match = re.search(string, person[i[1]].lower())
                        if match:
                            count += 1
                    except KeyError:
                        pass
                person[f'{i[1]}_count'] = count
                count = 0
        return search

    def analysis_groups(self):
        user_groups = api.groups.get(user_id=self.user_id[0]['id'], v='5.92')['items']
        users_info = User.analysis_interests(self)
        for i in users_info:
            try:
                users_groups = api.groups.get(user_id=i['id'], v='5.92')['items']
                len_mutual_groups = len(list(set(user_groups) & set(users_groups)))
                i['len_mutual_groups'] = len_mutual_groups
            except vk.exceptions.VkAPIError as e:
                if '6. Too many requests per second' in str(e):
                    time.sleep(1)
                else:
                    users_info.remove(i)
        for user in users_info[:]:
            if 'len_mutual_groups' not in user:
                users_info.remove(user)
        return users_info

    def analysis_of_weights(self):
        users_info = User.analysis_groups(self)
        for i in users_info:
            i['rating'] = i['common_count'] * 1.2 + i['interests_count'] * \
                          1.3 + i['music_count'] + i['movies_count'] * 1.4 + \
                          i['books_count'] * 1.25 + i['games_count'] * 1.35 +\
                          i['len_mutual_groups'] * 1.5
        users_info.sort(key=itemgetter('rating'), reverse=True)
        return users_info[:10]

    def profile_and_photo(self):
        users_info = User.analysis_of_weights(self)
        result = {}
        result['user'] = 'https://vk.com/id' + str(self.user_id[0]['id'])
        people_list = []
        for i in users_info:
            try:
                people = {}
                photo_list = []
                search = api.photos.get(owner_id=i['id'], album_id='profile',
                                        extended=1, v='5.92')
                for ph in search['items']:
                    photo_list.append({'likes': ph['likes']['count'],
                                       'photo': ph['sizes'][-1]['url']})
                photo_list.sort(key=itemgetter('likes'), reverse=True)
                people['profile'] = 'https://vk.com/id' + str(i['id'])
                people['photo'] = photo_list[:3]
                people_list.append(people)
            except vk.exceptions.VkAPIError as e:
                if '6. Too many requests per second' in str(e):
                    time.sleep(1)
        result['result'] = people_list
        json_vkinder(result)
        write_to_database(result)
        return result
