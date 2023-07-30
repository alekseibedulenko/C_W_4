from classes.abstract_class import WorkWithJson
from classes.clients.get_info_from_hh import Vacancy
from classes.clients.joint_class import VacancyJoint
from classes.clients.get_info_from_superjob import VacancySuperJob
from classes.error import InputError


def start_with_user():
    """Начало работы, приветствие и выбор платформы для поиска"""
    platforms = ["HeadHunter", "SuperJob"]
    chose_platforms = input("Здравствуйте, выберите платформу для поиска вакансий:\n"
                            f"1- {','.join(platforms)}\n"
                            f"2- {platforms[0]}\n"
                            f"3- {platforms[1]}\n"
                            "4- Выход\n")
    if chose_platforms == "1":
        print(f"Выбранные платформы - {','.join(platforms)} ")
        vacancies_from = VacancyJoint()
        return vacancies_from
    elif chose_platforms == "2":
        print(f"Выбранная платформа - {platforms[0]}")
        vacancies_from_hh = Vacancy()
        return vacancies_from_hh
    elif chose_platforms == "3":
        print(f"Выбранная платформа - {platforms[1]}")
        superjob_api = VacancySuperJob()
        return superjob_api
    elif chose_platforms == "4":
        print("Хорошего дня и удачного поиска!")
        return None
    else:
        raise InputError


def find_vacancy():
    """Поиск вакансий по ключевому слову и отображение по указанному количеству"""

    vacancies_from = start_with_user()
    if vacancies_from is not None:
        search_query = input("Введите ключевое слово для поиска вакансии: ")
        vacancies_from.get_vacancies(search_query)
        if not vacancies_from.get_vacancies(search_query):
            print(f"Вакансий с {search_query}. не найдено")
            return
        filter_words = input("Введите критерий сортировки вакансий:\n"
                                 "'Дата публикации' -- 1 \n"
                                 "'Название вакансии' -- 2 \n"
                                 "'Город' -- 3 \n")
        per_page = int(input("Введите количество вакансий для вывода: "))
        if isinstance(per_page, int):
            if filter_words == "1":
                print("Сортировка по дате публикации")
                return vacancies_from.sort_by('Дата публикации', per_page)
            elif filter_words == "2":
                print("Сортировка по названию:")
                return vacancies_from.sort_by('Название вакансии', per_page)
            elif filter_words == "3":
                print("Сортировка по городу")
                city = input("Введите название города: ")
                if vacancies_from.sort_by(city, per_page):
                    return vacancies_from.sort_by(city, per_page)
                else:
                    raise InputError
            else:
                raise InputError
        else:
            raise ValueError
    else:
        return None


def add_vacancy(vacancies):
    """Добавление вакансии в файл"""
    vacancies_from = WorkWithJson()
    vacancy_sort = vacancies
    if vacancy_sort is not None:
        add_vacancy = int(input(
            "Для добавления вакансии в  файл,укажите 'id вакансии': "))
        vacancy_add_list = []
        if isinstance(add_vacancy, int):
            for x in vacancy_sort:
                if x['id вакансии'] == add_vacancy:
                    vacancy_add = Vacancy(vacancy_id=x['id вакансии'],
                                          vacancy_name=x['Название вакансии'],
                                          vacancy_date=x['Дата публикации'],
                                          vacancy_url=x['https cсылка'],
                                          vacancy_salary=x['Заработная плата'],
                                          vacancy_city=x['Город'],
                                          vacancy_requirement=x['Требование'],
                                          vacancy_responsibility=x['Обязанности']
                                          )
                    vacancy_add_list.append(vacancy_add.to_json())
            vacancies_from.add_vacancy(vacancy_add_list)
            print("Вакансия добавлена в файл!")
        else:
            raise ValueError


def del_vacancy():
    """Удаление вакансий из файла"""
    vacancies_from = WorkWithJson()
    delete_vacancy = int(input(
        "Для удаления вакансии из файла,укажите 'id вакансии': "))
    if isinstance(delete_vacancy, int):
        result = vacancies_from.delete_vacancy(delete_vacancy)
        return result
    else:
        raise ValueError


def full_info():
    """Получение полной информации о вакансии из файла"""

    vacancies_from = WorkWithJson()
    id_vacancy = int(input("id вакансии: "))
    if isinstance(id_vacancy, int):
        print(f"Информация о вакансии с id {id_vacancy}: ")
        vacancies_from.get_vacancies_by(id_vacancy)
    else:
        raise ValueError


def comparison_by_salary():
    """Сравнение вакансий(которые добавлены в файл) по заработной плате"""

    vacancies_from = WorkWithJson()
    id_vac_x = int(input("Вакансия №1: "))
    id_vac_y = int(input("Вакансия №2: "))
    if isinstance(id_vac_x, int) and isinstance(id_vac_y, int):
        salary = vacancies_from.get_vacancies_by(id_vac_x, id_vac_y)
        vacancies_from.vacancy_salary = int(
            salary[0].split('-')[0]) if salary[0].split('-')[0].isdigit() else 0
        vacancies_from.other_salary = int(
            salary[1].split('-')[0]) if salary[1].split('-')[0].isdigit() else 0

        if vacancies_from.vacancy_salary >= vacancies_from.other_salary:
            print(f"Вакансия {id_vac_x} c заработной платой {vacancies_from.vacancy_salary},\n"
                  f"больше или равна вакансии {id_vac_y} c заработной платой {vacancies_from.other_salary}")
        else:
            print(f"Вакансия {id_vac_y} c заработной платой {vacancies_from.vacancy_salary},\n"
                  f"меньше или равна вакансии {id_vac_x} c заработной платой {vacancies_from.other_salary}")
    else:
        raise ValueError


def main():
    """Вывод найденных вакансий и дальнейшие действия с ними"""

    try:
        vacancy_sort = find_vacancy()
        if vacancy_sort is not None:
            print("Найденные вакансии:")
            for x in vacancy_sort:
                print(x)
            while True:
                next_move = int(input("Выберите дальнейшее действие: \n"
                                      "1 - добавление вакансии в json-файл\n"
                                      "2 - удаление вакансии из json-файла\n"
                                      "3 - получение информации о вакансии из файла\n"
                                      "4 - сравнение вакансий по заработной плате\n"
                                      "5 - выход\n"))

                if isinstance(next_move, int):
                    if next_move == 1:
                        add_vacancy(vacancy_sort)
                        continue
                    elif next_move == 2:
                        del_vacancy()
                        continue
                    elif next_move == 3:
                        print("Для получения полной информации о  вакансии по  укажите её id : ")
                        full_info()
                        continue
                    elif next_move == 4:
                        print("Для сравнения вакансий по заработной плате введите id вакансий:")
                        comparison_by_salary()
                        continue
                    elif next_move == 5:
                        print("Хорошего дня и удачного поиска!")
                        break
                else:
                    raise InputError
            return vacancy_sort
        else:
            return None
    except (InputError, ValueError) as error:
        print(error.message)
