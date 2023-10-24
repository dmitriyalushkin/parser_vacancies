from utils import HeadHunterAPI, SuperJobAPI, JSONSaver
import json

def user_interaction():
    '''Функция для взаимодействия с пользователем'''

    name = input('Введите вакансию: ')
    page = input('Введите кол-во вакансий: ')
    per_page = int(input('Введите страницу: '))

    platforma = input('введите платформу для поиска: (1 - HH, 2 - SJ, 3 - обе платформы)  ')

    if platforma == '3':
        while True:
            hh_instance = HeadHunterAPI(name, page, per_page)
            sj_instance = SuperJobAPI(name, page, per_page)
            vacancies = hh_instance.add_vacancy_hh() + sj_instance.add_vacancy_sj()
            json_saver = JSONSaver()
            json_saver.add_vacancies(vacancies, 'vacancies.json')

            for vacancy in vacancies:
                print(vacancy)

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platforma == '1':
        while True:
            hh_instance = HeadHunterAPI(name, page, per_page)
            vacancies = hh_instance.add_vacancy_hh()
            json_saver = JSONSaver()
            json_saver.add_vacancies(vacancies, 'hh.json')

            for vacancy in vacancies:
                print(vacancy)
            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platforma == '2':
        while True:
            sj_instance = SuperJobAPI(name, page, per_page)
            vacancies = sj_instance.add_vacancy_sj()
            json_saver = JSONSaver()
            json_saver.add_vacancies(vacancies, 'sj.json')

            for vacancy in vacancies:
                print(vacancy)

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

user_interaction()
# hh_api = HeadHunterAPI('python', 1, 1)
# superjob_api = SuperJobAPI('python', 1, 100000)
# print(hh_api >= superjob_api)