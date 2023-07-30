from datetime import datetime

from classes.abstract_class import GetInfo

import requests

from classes.error import InputError


class HeadHunterAPI(GetInfo):
    """Класс для получения вакансий с hh"""

    def __init__(self):
        """
        Инициализируемся по слову, которое вводит пользователь
        """
        self.keyword = None
        self.per_page = None
        self.info = None

    def get_vacancies(self, keyword: str):
        """
        Метод в котором получаем вакансии по заданным параметрам
        """
        self.keyword = keyword
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': self.keyword
        }
        response = requests.get(url, params=params)
        vacancies = response.json()
        return vacancies


class Vacancy(HeadHunterAPI, InputError):
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
        for item in data['items']:
            salary = item['salary']
            salary_range = f"{salary['from']}-{salary['to']}, валюта {salary['currency']}" if salary and salary[
                'from'] and salary['to'] else "Не указано"
            date = item['published_at']
            date_str = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
            publish_time = date_str.strftime('%m-%d-%Y')
            vacancy = {
                "id вакансии": int(item['id']),
                "Название вакансии": item['name'],
                "Дата публикации": publish_time,
                "Заработная плата": salary_range,
                "Город": item["area"]["name"],
                "Требование": item['snippet']['requirement'],
                "Обязанности": item['snippet']['responsibility'],
                "https cсылка": item['url']
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

        salary_self = int(self.vacancy_salary)
        salary_other = int(other.vacancy_salary)
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
