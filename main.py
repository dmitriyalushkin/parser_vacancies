from utils import HeadHunterAPI, SuperJobAPI
import json

def user_interaction():
    '''Функция для взаимодействия с пользователем'''

    name = input('Введите вакансию: ')
    top_n = input('Введите кол-во вакансий: ')
    page = int(input('Введите страницу: '))
    hh_instance = HeadHunterAPI(name, page, top_n)
    sj_instance = SuperJobAPI(name, page, top_n)
    combined_dict = {'HH': hh_instance.add_vacancy_hh(), 'SJ': sj_instance.add_vacancy_sj()}

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

    platforma = input('введите платформу для поиска: (1 - HH, 2 - SJ, 3 - обе платформы)  ')

    if platforma == '3':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.add_vacancy_hh()
            sj_data = sj_instance.add_vacancy_sj()

            combined_dict['HH'] = hh_data
            combined_dict['SJ'] = sj_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform, data in combined_dict.items():
                print(f"\n \033Платформа: {platform}")
                for item in data:
                    print(
                        f"id - {item['id']}\nДолжность - {item['name']}\nЗ.п от - {item['salary_ot']}\nЗ.п до - {item['salary_do']}\nОписание - {item['responsibility']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break
    elif platforma == '1':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.add_vacancy_hh()

            combined_dict['HH'] = hh_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['HH']:
                print(
                    f"\nid - {platform['id']}\nДолжность - {platform['name']}\nЗ.п от - {platform['salary_ot']}\nЗ.п до - {platform['salary_do']}\nОписание - {platform['responsibility']}\n")
            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

    elif platforma == '2':
        while True:
            hh_instance.page = page
            sj_instance.page = page
            hh_data = hh_instance.add_vacancy_hh()
            sj_data = sj_instance.add_vacancy_sj()

            combined_dict['HH'] = hh_data
            combined_dict['SJ'] = sj_data

            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(combined_dict, file, ensure_ascii=False, indent=2)

            for platform in combined_dict['SJ']:
                print(
                    f"\nid - {platform['id']}\nДолжность - {platform['name']}\nЗ.п от - {platform['salary_ot']}\nЗ.п до - {platform['salary_do']}\nОписание - {platform['responsibility']}\n")

            a = input('перейти на следующую страницу? y/n ')
            if a == 'y':
                page += 1
            else:
                break

user_interaction()