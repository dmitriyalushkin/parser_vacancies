from abc import ABC, abstractmethod

import requests
import json
import os

SECRET_KEY = os.getenv('X-Api-App-Id')


class ApiClient(ABC):
    """Класс для получения вакансий с помощью API"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class Vacancy:
    '''Класс для работы с вакансиями'''

    def __init__(self, id, name, salary_ot, salary_do, responsibility):
        self.id = id
        self.name = name
        self.salary_ot = salary_ot
        self.salary_do = salary_do
        self.responsibility = responsibility

    def __str__(self):
        return f"\nid - {self.id}\nДолжность - {self.name}\n" \
               f"З.п от - {self.salary_ot}\nЗ.п до - {self.salary_do}\n" \
               f"Описание - {self.responsibility}\n"

    def __ge__(self, other):
        return self.salary_ot >= other.salary_ot

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'salary_ot': self.salary_ot,
            'salary_do': self.salary_do,
            'responsibility': self.responsibility
        }


class HeadHunterAPI(ApiClient):
    """Получает вакансию от API HeadHunter"""

    def __init__(self, name, page, per_page):
            self.name = name
            self.page = page
            self.per_page = per_page
            self.url = 'https://api.hh.ru'

    def get_vacancies(self):
            data = requests.get(f'{self.url}/vacancies', params={'text': self.name,
                                                                 'page': self.page,
                                                                 'per_page': self.per_page}).json()
            return data

    def add_vacancy_hh(self):
        data = self.get_vacancies()
        vacancies = []
        for hh_vacancy in data['items']:
            vacancy = Vacancy(id=hh_vacancy['id'],
                              name=hh_vacancy['name'],
                              salary_ot=hh_vacancy['salary']['from'] if hh_vacancy['salary'] else None,
                              salary_do=hh_vacancy['salary']['to'] if hh_vacancy['salary'] else None,
                              responsibility=hh_vacancy['snippet']['requirement'])
            vacancies.append(vacancy)

        return vacancies


class SuperJobAPI(ApiClient):
    """Получает вакансию от API SuperJob"""
    def __init__(self, name, page, per_page):
        self.name = name
        self.page = page
        self.per_page = per_page
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self):
        headers = {
                    'X-Api-App-Id': os.getenv('X-Api-App-Id'),
                    }
        data = requests.get(self.url, headers=headers, params={'keywords': self.name,
                                                               'page': self.page,
                                                               'count': self.per_page}).json()
        return data

    def add_vacancy_sj(self):
        data = self.get_vacancies()
        vacancy_list_SJ = []
        for sj_vacancy in data['objects']:
            vacancy = Vacancy(
                id=sj_vacancy['id'],
                name=sj_vacancy['profession'],
                salary_ot=sj_vacancy['payment_from'] if sj_vacancy['payment_from'] else None,
                salary_do=sj_vacancy['payment_to'] if sj_vacancy['payment_to'] else None,
                responsibility=sj_vacancy['candidat']
            )
            vacancy_list_SJ.append(vacancy)
            return vacancy_list_SJ



class VacanciesJSON(ABC):
    @abstractmethod
    def add_vacancies(self, data, filename):
        pass


    @abstractmethod
    def add_vacancy(self, vacancy, filename):
        pass


class JSONSaver(VacanciesJSON):
    '''Класс для сохранения информации о вакансиях в JSON-файл'''
    def add_vacancies(self, vacancies, filename):

        for vacancy in vacancies:
            self.add_vacancy(vacancy, filename)

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            data = json.dump(vacancy.to_json(), file, indent=2, ensure_ascii=False)
        return data











# hh_api = HeadHunterAPI('python', 1, 1)
# hh_vacancies = hh_api.get_vacancies()
# print(hh_vacancies)
# superjob_api = SuperJobAPI('python', 1, 100000)
# superjob_vacancies = superjob_api.get_vacancies()
# print(superjob_vacancies)
# jsonsaver = JSONSaver()
# print(jsonsaver.add_vacancy_headhunter(hh_vacancies))
# print(jsonsaver.add_vacancy_superjob(superjob_vacancies))
# print(hh_api >= superjob_api)


