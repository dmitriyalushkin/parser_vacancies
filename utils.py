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


class HeadHunterAPI(Vacancy, ApiClient):
    """Получает вакансию от API HeadHunter"""

    def __init__(self, name, page, top_n):
            super().__init__(name, page, top_n)
            self.url = 'https://api.hh.ru'

    def get_vacancies(self):
            data = requests.get(f'{self.url}/vacancies', params={'text': 'python', 'page': 1, 'per_page': 10}).json()
            return data

    def add_vacancy_hh(self):
        data = self.get_vacancies()
        vacancies = []
        for vacancy in data['items']:
            head_hunter = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'salary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility']
            }
            vacancies.append(head_hunter)

        return vacancies


class SuperJobAPI(Vacancy, ApiClient):
    """Получает вакансию от API SuperJob"""
    def __init__(self, name, page, top_n):
        super().__init__(name, page, top_n)
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self):
        headers = {
                    'X-Api-App-Id': os.getenv('X-Api-App-Id'),
                    }
        data = requests.get(self.url, headers=headers, params={'keywords': self.name, 'page': self.page, 'count': self.top_n}).json()
        return data

    def add_vacancy_sj(self):
        data = self.get_vacancies()
        vacancy_list_SJ = []
        for i in data['objects']:
            super_job = {
                        'id': i['id'],
                        'name': i.get('profession', ''),
                        'salary_ot': i.get('payment_from', '') if i.get('payment_from') else None,
                        'salary_do': i.get('payment_to') if i.get('payment_to') else None,
                        'responsibility': i.get('candidat').replace('\n', '').replace('•', '') if i.get('candidat') else None
                    }
            vacancy_list_SJ.append(super_job)
            return vacancy_list_SJ










# hh_api = HeadHunterAPI('python', 1, 100000)
# hh_vacancies = hh_api.get_vacancies()
# print(hh_vacancies)
superjob_api = SuperJobAPI('python', 1, 100000)
superjob_vacancies = superjob_api.add_vacancy_sj()
print(superjob_vacancies)

