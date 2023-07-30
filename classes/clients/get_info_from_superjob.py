
from datetime import datetime

import requests

from classes.abstract_class import GetInfo
from classes.error import InputError


class SuperJobAPI(GetInfo):
    """Класс и метод для получения вакансий с superjob"""

    def __init__(self):
        """
        Инициализируемся по слову, которое вводит пользователь
        """
        self.keyword = None
        self.per_page = None
        self.info = None

    def get_vacancies(self, keyword):
        """
        Метод в котором получаем вакансии по заданным параметрам
        """
        key = "v3.r.137714112.fe9ac30bcf1184142d454fc94758660d0f54ffc2.0514b7665fe714e0954324d4e82d1a75d209f011"
        self.keyword = keyword
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': key
        }
        params = {
            'keyword': keyword
        }
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()
        return data


class VacancySuperJob(SuperJobAPI, InputError):
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy_id=None, vacancy_name=None, vacancy_date=None,
                 vacancy_url=None, vacancy_salary=None,
                 vacancy_city=None, vacancy_requirement=None,
                 vacancy_responsibility=None):
        """
        Инициализация по параметрам
        """
        try:
            self.vacancy_id = vacancy_id
            self.vacancy_name = vacancy_name
            self.vacancy_date = vacancy_date
            self.vacancy_url = vacancy_url
            self.vacancy_salary = vacancy_salary
            self.vacancy_city = vacancy_city
            self.vacancy_requirement = vacancy_requirement
            self.vacancy_responsibility = vacancy_responsibility
        except InputError as m:
            print(m.message)

    def sorted_vacancy(self):
        """
        Метод сортировки информации из api hh в универсальный
        """
        data = self.get_vacancies(self.keyword)
        sorted_vacancy = []
        for item in data['objects']:
            salary = f"{item['payment_from']}-{item['payment_to']}, валюта {item['currency']}"
            date_str_from = datetime.fromtimestamp(item['date_published'])
            publish_time = date_str_from.strftime('%m-%d-%Y')
            info = str(item['candidat'])
            start_index_requir = info.find('Обязанности')
            start_index_resp = info.find('Требования')
            end_index_requir = info.find('Требования') if info.find('Требовани') != -1 else len(info)
            end_index_resp = info.find('Условия:') if info.find('Условия:') != -1 else len(info)
            requirement = info[start_index_requir:end_index_requir] if start_index_requir != -1 \
                                                                       and end_index_requir != -1 else info
            responsibility = info[start_index_resp:end_index_resp] if start_index_resp != -1 \
                                                                      and end_index_resp != -1 else info
            vacancy = {
                "id вакансии": int(item['id']),
                "Название вакансии": item['profession'],
                "Дата публикации": publish_time,
                "Заработная плата": salary,
                "Город": item['town']['title'],
                "Требование": responsibility,
                "Обязанности": requirement,
                "https cсылка": item['link']
            }

            sorted_vacancy.append(vacancy)
        return sorted_vacancy

    def sort_by(self, info, per_page):
        """
        Сортировка и определение количества выводимых вакансий по заданным параметрам
        """

        self.per_page = per_page
        self.info = info
        sorted_vacancy = self.sorted_vacancy()
        if sorted_vacancy:
            sorted_by_city = []
            for x in sorted_vacancy:
                if self.info is not None and self.info in x['Город']:
                    sorted_by_city.append(x)
                else:
                    sorted_vacancy.sort(key=lambda x: x.get(self.info, ''), reverse=True)
            if len(sorted_by_city) > 0:
                for x in sorted_by_city:
                    sorted_by_city.sort(key=lambda x: x.get('Дата публикации', ''), reverse=True)
                return sorted_by_city[:self.per_page]
            else:
                return sorted_vacancy[:self.per_page]
        else:
            raise InputError

    def to_json(self):
        """
        Преобразование объекта Vacancy в словарь
        """

        return {
            "id вакансии:": self.vacancy_id,
            "Название вакансии:": self.vacancy_name,
            "Дата публикации:": self.vacancy_date,
            "https cсылка:": self.vacancy_url,
            "Заработная плата:": self.vacancy_salary,
            "Город:": self.vacancy_city,
            "Требование:": self.vacancy_requirement,
            "Обязанности:": self.vacancy_responsibility
        }

    def __le__(self, other):
        """
        Магический метод для проверки заработной платы <=
        """
        salary_self = int(str(self.vacancy_salary).split('-')[0])
        salary_other = int(str(other.vacancy_salary).split('-')[0])
        if salary_self <= salary_other:
            return True
        else:
            raise ValueError

    def __ge__(self, other):
        """
        Магический метод для проверки заработной платы >=
        """

        salary_other = int(other.vacancy_salary)
        if self.vacancy_salary >= salary_other:
            return True
        else:
            raise ValueError
