import telebot
import sqlite3
from keyboards import *

bot = telebot.TeleBot("")

# Подключение к базе данных
database = sqlite3.connect("contacts.db")
cursor = database.cursor()

# Создание таблицы контактов, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  Имя TEXT,
                  Фамилия TEXT,
                  Телефон TEXT,
                  Email TEXT,
                  Комментарий TEXT)''')
database.commit()
database.close()

name, surname, phone, email, comment = "Без имени", "Без фамилии", "Без телефона", "Без email", "Без комментария"

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/start", "Запуск бота"),
        telebot.types.BotCommand("/help", "Помощь")
    ]
)


# Команды:

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f'<i>Приветствую вас <b><u>{message.from_user.first_name}</u></b>, в нашем боте вы можете '
                     f'хранить и редактировать свои контакты!</i>',
                     parse_mode='html')
    keyboard = create_main_menu_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help(message):
    with open('help.txt', 'r', encoding='utf-8') as file:
        instructions = file.read()
    bot.send_message(message.chat.id, instructions)


@bot.message_handler(func=lambda message: message.text == "Добавить контакт")
def add_contact(message):
    keyboard = create_add_contact_submenu_keyboard()
    bot.send_message(message.chat.id, "Введите имя:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_name)


# Ввод данных контакта по очереди
def get_name(message):
    global name
    if message.text == "Пропустить":
        name = "Без имени"
        bot.send_message(message.chat.id, "Введите фамилию:")
        bot.register_next_step_handler(message, get_surname)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    else:
        name = message.text
        bot.send_message(message.chat.id, "Введите фамилию:")
        bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    if message.text == "Пропустить":
        surname = "Без фамилии"
        bot.send_message(message.chat.id, "Введите телефон:")
        bot.register_next_step_handler(message, get_phone)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    else:
        surname = message.text
        bot.send_message(message.chat.id, "Введите телефон:")
        bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    global phone
    if message.text == "Пропустить":
        phone = "Без телефона"
        bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(message, get_email)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    else:
        phone = message.text
        bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(message, get_email)


def get_email(message):
    global email
    if message.text == "Пропустить":
        email = "Без email"
        bot.send_message(message.chat.id, "Введите комментарий:")
        bot.register_next_step_handler(message, get_comment)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    else:
        email = message.text
        bot.send_message(message.chat.id, "Введите комментарий:")
        bot.register_next_step_handler(message, get_comment)


def get_comment(message):
    global comment
    if message.text == "Пропустить":
        comment = "Без комментарий"
        keyboard = add_contact_to_database_keyboard()
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        bot.register_next_step_handler(message, add_contact_to_database)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    else:
        comment = message.text
        keyboard = add_contact_to_database_keyboard()
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        bot.register_next_step_handler(message, add_contact_to_database)


# Функция для добавления контакта в базу данных
def add_contact_to_database(message):
    if message.text == "Пропустить":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    elif message.text == "Записать контакт":
        database = sqlite3.connect("contacts.db")
        cursor = database.cursor()
        cursor.execute("INSERT INTO contacts (Имя, Фамилия, Телефон, Email, Комментарий) VALUES (?, ?, ?, ?, ?)",
                       (name, surname, phone, email, comment))
        contact = cursor.lastrowid
        database.commit()
        database.close()
        bot.send_message(message.chat.id,
                         f"<b><u>Контакт №:</u></b> <b>{contact}</b> <pre>{name}\n{surname}\n{phone}\n{email}\n"
                         f"{comment}</pre>\n <b><u>Успешно добавлен!</u></b>", parse_mode='html')
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


# Поиск контакта по любому полю
@bot.message_handler(func=lambda message: message.text == "Поиск контакта")
def search_contact(message):
    keyboard = create_search_contact_submenu_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_field_search_contact)


def get_field_search_contact(message):
    if message.text == "Общий поиск":
        bot.send_message(message.chat.id, "Введите любые данные контакта:")
        bot.register_next_step_handler(message, search_in_all)
    elif message.text == "ID":
        bot.send_message(message.chat.id, "Введите номер контакта:")
        bot.register_next_step_handler(message, search_field_contact, message_text="ID")
    elif message.text == "Имя":
        bot.send_message(message.chat.id, "Введите имя:")
        bot.register_next_step_handler(message, search_field_contact, message_text="Имя")
    elif message.text == "Фамилия":
        bot.send_message(message.chat.id, "Введите фамилию:")
        bot.register_next_step_handler(message, search_field_contact, message_text="Фамилия")
    elif message.text == "Телефон":
        bot.send_message(message.chat.id, "Введите телефон:")
        bot.register_next_step_handler(message, search_field_contact, message_text="Телефон")
    elif message.text == "Email":
        bot.send_message(message.chat.id, "Введите email:")
        bot.register_next_step_handler(message, search_field_contact, message_text="Email")
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


def search_in_all(message):
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    try:
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        keyword = message.text
        cursor.execute("SELECT * FROM contacts")
        matching_contacts = [contact for contact in contacts if
                             keyword.lower() in [str(field).lower() for field in contact[0:]]]
        if len(matching_contacts) > 0:
            for contact in matching_contacts:
                bot.send_message(message.chat.id,
                                 f"<u><b>№ контакта:</b></u> <b>{contact[0]}</b>\n<u>Имя:</u> <pre>{contact[1]}</pre>\n<u"
                                 f">Фамилия:</u> <pre>{contact[2]}</pre>\n<u>Телефон:</u> <pre>"
                                 f"{contact[3]}</pre>\n<u>Email:</u> <pre>{contact[4]}</pre>\n<u>Комментарий:</u> <pre>"
                                 f"{contact[5]}</pre>\n===============================",
                                 parse_mode='html')
            keyboard = create_search_contact_submenu_keyboard()
            bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_field_search_contact)
        else:
            bot.send_message(message.chat.id, f"Контакт {message.text} не найден.")
            keyboard = create_search_contact_submenu_keyboard()
            bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_field_search_contact)
    except sqlite3.OperationalError:
        bot.send_message(message.chat.id, "Контакт не найден.")
        keyboard = create_search_contact_submenu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_field_search_contact)


def search_field_contact(message, message_text):
    global contact
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    try:
        if message_text == "ID":
            contact_id = message.text
            cursor.execute("SELECT * FROM contacts WHERE ID = ?", (contact_id,))
            contact = cursor.fetchone()
        elif message_text == "Имя":
            name = message.text
            cursor.execute("SELECT * FROM contacts WHERE Имя = ?", (name,))
            contact = cursor.fetchone()
        elif message_text == "Фамилия":
            surname = message.text
            cursor.execute("SELECT * FROM contacts WHERE Фамилия = ?", (surname,))
            contact = cursor.fetchone()
        elif message_text == "Телефон":
            phone = message.text
            cursor.execute("SELECT * FROM contacts WHERE Телефон = ?", (phone,))
            contact = cursor.fetchone()
        elif message_text == "Email":
            email = message.text
            cursor.execute("SELECT * FROM contacts WHERE Email = ?", (email,))
            contact = cursor.fetchone()
        if contact:
            bot.send_message(message.chat.id,
                             f"<u><b>№ контакта:</b></u> <b>{contact[0]}</b>\n<u>Имя:</u> <pre>{contact[1]}</pre>\n<u"
                             f">Фамилия:</u> <pre>{contact[2]}</pre>\n<u>Телефон:</u> <pre>"
                             f"{contact[3]}</pre>\n<u>Email:</u> <pre>{contact[4]}</pre>\n<u>Комментарий:</u> <pre>"
                             f"{contact[5]}</pre>\n===============================",
                             parse_mode='html')
            keyboard = create_search_contact_submenu_keyboard()
            bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_field_search_contact)
        else:
            bot.send_message(message.chat.id, f"Контакт {message.text} не найден.")
            keyboard = create_search_contact_submenu_keyboard()
            bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
            bot.register_next_step_handler(message, get_field_search_contact)
    except sqlite3.OperationalError:
        bot.send_message(message.chat.id, "Контакт не найден.")
        keyboard = create_search_contact_submenu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_field_search_contact)


# Показать все контакты
@bot.message_handler(func=lambda message: message.text == "Показать все контакты")
def show_all_contacts(message):
    try:
        database = sqlite3.connect("contacts.db")
        cursor = database.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        for contact in contacts:
            bot.send_message(message.chat.id,
                             f"<u><b>№ контакта:</b></u> <b>{contact[0]}</b>\n<u>Имя:</u> <pre>{contact[1]}</pre>\n<u"
                             f">Фамилия:</u> <pre>{contact[2]}</pre>\n<u>Телефон:</u> <pre>"
                             f"{contact[3]}</pre>\n<u>Email:</u> <pre>{contact[4]}</pre>\n<u>Комментарий:</u> <pre>"
                             f"{contact[5]}</pre>\n===============================",
                             parse_mode='html')
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    except sqlite3.OperationalError:
        bot.send_message(message.chat.id, "Контакты не найдены. Импортируйте файл с контактами или добавьте по одному.")
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


# Редактировать контакт
@bot.message_handler(func=lambda message: message.text == "Редактировать контакт")
def edit_contact(message):
    bot.send_message(message.chat.id, "Введите ID контакта для редактирования:")
    bot.register_next_step_handler(message, process_edit_contact)


def process_edit_contact(message):
    contact_id = message.text
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM contacts WHERE ID = ?", (contact_id,))
    contact = cursor.fetchone()
    if contact:
        bot.send_message(message.chat.id,
                         f"Выбран контакт с ID: {contact[0]}\nИмя: {contact[1]}\nФамилия: {contact[2]}\nТелефон: "
                         f"{contact[3]}\nEmail: {contact[4]}\nКомментарий: {contact[5]}")
        keyboard = create_edit_contact_submenu_keyboard()
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
        bot.register_next_step_handler(message, process_edit_contact_action, contact_id)
    else:
        bot.send_message(message.chat.id, f"Контакт с ID {contact_id} не найден.")
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


def process_edit_contact_action(message, contact_id):
    action = message.text
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    if action == "Изменить контакт":
        bot.send_message(message.chat.id, f"Текущая информация о контакте с ID {contact_id}:")
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cursor.fetchone()
        bot.send_message(message.chat.id,
                         f"<b>ID:</b> {contact[0]}\n<b>Имя:</b> {contact[1]}\n<b>Фамилия:</b>"
                         f" {contact[2]}\n<b>Телефон:</b> {contact[3]}\n<b>Email</b>: {contact[4]}\n<b>Комментарий:</b> "
                         f"{contact[5]}", parse_mode='html')
        keyboard = field_edit_contact_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
        bot.register_next_step_handler(message, field_edit_contact, contact_id)
    elif action == "Удалить контакт":
        cursor.execute("DELETE FROM contacts WHERE ID = ?", (contact_id,))
        database.commit()
        bot.send_message(message.chat.id, f"Контакт с ID {contact_id} успешно удален.")
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    elif action == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


def field_edit_contact(message, contact_id):
    if message.text == "Изменить Имя":
        bot.send_message(message.chat.id, "Введите новое Имя:")
        bot.register_next_step_handler(message, process_edit_contact_field, contact_id, "Имя")
    elif message.text == "Изменить Фамилию":
        bot.send_message(message.chat.id, "Введите новую фамилию:")
        bot.register_next_step_handler(message, process_edit_contact_field, contact_id, "Фамилия")
    elif message.text == "Изменить Телефон":
        bot.send_message(message.chat.id, "Введите новый телефон:")
        bot.register_next_step_handler(message, process_edit_contact_field, contact_id, "Телефон")
    elif message.text == "Изменить Email":
        bot.send_message(message.chat.id, "Введите новый email:")
        bot.register_next_step_handler(message, process_edit_contact_field, contact_id, "Email")
    elif message.text == "Изменить Комментарий":
        bot.send_message(message.chat.id, "Введите новый комментарий:")
        bot.register_next_step_handler(message, process_edit_contact_field, contact_id, "Комментарий")
    elif message.text == "Назад":
        keyboard = create_main_menu_keyboard()
        bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


def process_edit_contact_field(message, contact_id, field):
    new_value = message.text
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    cursor.execute(f"UPDATE contacts SET {field} = ? WHERE ID = ?", (new_value, contact_id))
    database.commit()
    bot.send_message(message.chat.id, f"Поле '{field}' успешно обновлено.")
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    contact = cursor.fetchone()
    bot.send_message(message.chat.id,
                     f"<b>ID:</b> {contact[0]}\n<b>Имя:</b> {contact[1]}\n<b>Фамилия:</b>"
                     f" {contact[2]}\n<b>Телефон:</b> {contact[3]}\n<b>Email</b>: {contact[4]}\n<b>Комментарий:</b> "
                     f"{contact[5]}", parse_mode='html')
    keyboard = field_edit_contact_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)
    bot.register_next_step_handler(message, field_edit_contact, contact_id)


# Импорт контактов
@bot.message_handler(func=lambda message: message.text == "Импорт контактов")
def import_contacts(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Пришлите файл с контактами в формате:\n\n<b>имя,фамилия,телефон,email,"
                              "комментарий</b>\n\n"
                              "В качестве разделителя между значениями используйте\nзапятую <b>,</b> без пробелов.\n\n"
                              "Чтобы пропустить значение, оставьте запятую без пробела.", parse_mode='html')
    bot.register_next_step_handler(message, handle_import)


@bot.message_handler(content_types=['document'])
def handle_import(message):
    try:
        if message.document is None:
            bot.reply_to(message, "Пожалуйста, прикрепите файл с контактами.")
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('imported_contacts.txt', 'wb') as file:
            file.write(downloaded_file)
        print("Файл с контактами успешно загружен.")
        import_contacts_from_file('imported_contacts.txt')
        bot.reply_to(message, "Контакты успешно импортированы в базу данных.")
    except Exception:
        bot.reply_to(message, "Произошла ошибка при импорте контактов. Пожалуйста, проверьте формат импорта и "
                              "повторите попытку.")


def import_contacts_from_file(filename):
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            name, surname, phone, email, comment = line.strip().split(',')
            cursor.execute("INSERT INTO contacts (Имя, Фамилия, Телефон, Email, Комментарий) VALUES (?, ?, ?, ?, ?)",
                           (name, surname, phone, email, comment))
            print(f"Импорт контакта: {name}, {surname}, {phone}, {email}, {comment}")
    database.commit()
    database.close()


@bot.message_handler(func=lambda message: message.text == "Экспорт контактов")
def export_contacts(message):
    chat_id = message.chat.id
    export_contacts_to_file(f'exported_contacts_{message.from_user.username}.txt')
    bot.send_document(chat_id, open(f'exported_contacts_{message.from_user.username}.txt', 'rb'))
    bot.reply_to(message, "Контакты успешно экспортированы в файл.")


def export_contacts_to_file(export_file):
    database = sqlite3.connect("contacts.db")
    cursor = database.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    cursor.close()
    database.close()

    with open(export_file, 'w', encoding='utf-8') as file:
        for contact in contacts:
            file.write(f"{contact[0]} - {contact[1]}, {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}\n")

    return contacts


@bot.message_handler(func=lambda message: message.text == "Пропустить")
def get_cancel(message):
    keyboard = create_main_menu_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Назад")
def go_back(message):
    keyboard = create_main_menu_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Отмена")
def cancel(message):
    keyboard = create_main_menu_keyboard()
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
