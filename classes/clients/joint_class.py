from datetime import datetime

from classes.clients.get_info_from_hh import Vacancy
from classes.clients.get_info_from_superjob import VacancySuperJob
from classes.error import InputError


class VacancyJoint(VacancySuperJob,Vacancy):
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
        data_superjob = super(VacancySuperJob, self).get_vacancies(self.keyword)
        data_hh = super(Vacancy, self).get_vacancies(self.keyword)
        sorted_vacancy = []
        if data_superjob:
            for item in data_superjob['objects']:
                salary_from = item['payment_from']
                salary_to =item['payment_to']
                salary = f"{salary_from}-{salary_to}, валюта {item['currency']}"
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
        if data_hh:
            for item in data_hh['items']:
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