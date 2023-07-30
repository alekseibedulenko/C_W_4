class InputError(Exception):
    """Пользовательский класс с выводом исключений"""
    def __init__(self):
        """
        Инициализация исключения
        """
        self.message = "Ошибка ввода данных"