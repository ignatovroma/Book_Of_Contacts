from telebot import types


# Клавиатура главного меню
def create_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add("Добавить контакт", "Поиск контакта")
    keyboard.add("Показать все контакты", "Редактировать контакт")
    keyboard.add("Импорт контактов", "Экспорт контактов")
    return keyboard


# Клавиатура подменю добавления контакта
def create_add_contact_submenu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    # keyboard.add("Имя", "Фамилия", "Телефон", "Email", "Комментарий")
    keyboard.add("Пропустить", "Назад")
    return keyboard


def add_contact_to_database_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("Пропустить", "Записать контакт", "Назад")
    return keyboard


# Клавиатура подменю поиска контакта
def create_search_contact_submenu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("Общий поиск", "ID", "Имя", "Фамилия", "Телефон", "Email", )
    keyboard.add("Назад")
    return keyboard


# Клавиатура подменю редактирования контакта
def create_edit_contact_submenu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("Изменить контакт", "Удалить контакт", "Назад")
    return keyboard


def field_edit_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("Изменить Имя", "Изменить Фамилию", "Изменить Телефон", "Изменить Email", "Изменить Комментарий")
    keyboard.add("Назад")
    return keyboard
