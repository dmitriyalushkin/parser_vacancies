from abc import ABC, abstractmethod

import requests

import os

SECRET_KEY = os.getenv('X-Api-App-Id')


class ApiClient(ABC):
    """Класс для получения вакансий с помощью API"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class Vacancy:
    def __init__(self, name, page, top_n):
        self.name = name
        self.page = page
        self.top_n = top_n

    def __repr__(self):
        return f'{self.name}'










# hh_api = HeadHunterAPI('python', 1, 100000)
# hh_vacancies = hh_api.get_vacancies()
# print(hh_vacancies)
# superjob_api = SuperJobAPI('python', 1, 100000)
# superjob_vacancies = superjob_api.add_vacancy_sj()
# print(superjob_vacancies)

