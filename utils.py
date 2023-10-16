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
    def __init__(self, name, page, top_n):
        self.name = name
        self.page = page
        self.top_n = top_n

    def __repr__(self):
        return f'{self.name}'

    def __ge__(self, other):
        return self.top_n >= other.top_n



class HeadHunterAPI(Vacancy, ApiClient):
    """Получает вакансию от API HeadHunter"""

    def __init__(self, name, page, top_n):
            super().__init__(name, page, top_n)
            self.url = 'https://api.hh.ru'

    def get_vacancies(self):
            data = requests.get(f'{self.url}/vacancies', params={'text': self.name, 'page': self.page, 'per_page': self.top_n}).json()
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



class VacanciesJSON(ABC):
    @abstractmethod
    def add_vacancy_headhunter(self):
        pass

    @abstractmethod
    def add_vacancy_superjob(self):
        pass

class JSONSaver(VacanciesJSON):
    def add_vacancy_headhunter(self, data):
        with open('hh.json', 'a', encoding='utf-8') as file:
            data_hh = json.dump(data, file, indent=2, ensure_ascii=False)
        return data_hh

    def add_vacancy_superjob(self, data):
        with open('sj.json', 'a', encoding='utf-8') as file:
            data_sj = json.dump(data, file, indent=2, ensure_ascii=False)
        return data_sj









hh_api = HeadHunterAPI('python', 1, 1)
hh_vacancies = hh_api.get_vacancies()
# print(hh_vacancies)
# superjob_api = SuperJobAPI('python', 1, 100000)
# superjob_vacancies = superjob_api.add_vacancy_sj()
# print(superjob_vacancies)
jsonsaver = JSONSaver()
print(jsonsaver.add_vacancy_headhunter(hh_vacancies))
# print(jsonsaver.add_vacancy_superjob(superjob_vacancies))


