import pickle
from address_book import AddressBook, InvalidBirthDateFormatException, InvalidPhoneException, \
    Record, InvalidEmailException
from notes_book import NotesBook, Note
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.formatted_text import FormattedText
from colorama import init, Fore


init()

def parse_input(user_input):
    """
    Розбирає введений користувачем рядок і повертає команду та аргументи.

    Args:
        user_input (str): Рядок введення від користувача.

    Returns:
        tuple: Кортеж, що містить команду та аргументи.
    """
    if len(user_input) > 0:
        cmd, *args = user_input.split()
    else:
        cmd, *args = '', []
    cmd = cmd.strip().lower()
    return cmd, *args


def note_error(func):
    """
    Декоратор, який перехоплює винятки ValueError та повертає повідомлення про помилку.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)

    return inner


def base_input_validator(func):
    """
    Декоратор, який перехоплює певні винятки, пов'язані з перевіркою контактів.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"{Fore.RED}No such contact."
        except IndexError:
            return f"{Fore.BLUE}Give me name please."
        except InvalidPhoneException:
            return f"{Fore.RED}Phone number length should be 10."
        except InvalidEmailException:
            return f"{Fore.RED}Please provide a valid email."
        except InvalidBirthDateFormatException:
            return f"{Fore.RED}Birthday should have format DD.MM.YYYY."

    return inner


def add_contact_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані з додаванням контакту.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and phone please."

    return inner


def change_phone_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані зі зміною номера телефону.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name, old phone and new phone please."

    return inner


def add_birthday_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані з додаванням дня народження.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and birthday please."

    return inner


def birthdays_input_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані з введенням кількості днів.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            params = args[0]
            if (len(params) > 0):
                days_count = int(params[0])
                if (days_count < 1):
                    return f"{Fore.BLUE}Give me the number of days > 0"

            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me the number of days > 0"

    return inner


def add_email_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані з додаванням електронної адреси.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and email please."

    return inner


def change_email_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані зі зміною електронної адреси.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name, old email and new email please."

    return inner


def add_address_validator(func):
    """
    Декоратор, який перехоплює винятки ValueError, пов'язані з додаванням адреси.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            # args after name
            address_parts = args[0][1:]
            if (len(address_parts) < 1):
                raise ValueError
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and address please."

    return inner


def find_contact_validator(func):
    """
    Декоратор, який перехоплює винятки IndexError, пов'язані з пошуком контакту.

    Args:
        func (callable): Функція для декорування.

    Returns:
        callable: Декорована функція.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"{Fore.BLUE}Give me search word please."

    return inner


@add_contact_validator
@base_input_validator
def add_contact(args, book: AddressBook):
    """
    Додає контакт до адресної книги.

    Args:
        args (list): Список аргументів, включаючи ім'я та номер телефону.

    Returns:
        str: Повідомлення про успішне додавання контакту.
    """
    name, phone = args

    try:
        new_record = book.find(name)
    except KeyError:
        new_record = Record(name)

    new_record.add_phone(phone)
    book.add_record(new_record)
    return f"{Fore.GREEN}Contact has been added."


@base_input_validator
def delete_contact(args, book: AddressBook):
    """
    Видаляє контакт з адресної книги.

    Args:
        args (list): Список аргументів, включаючи ім'я контакту.

    Returns:
        str: Повідомлення про успішне видалення контакту.
    """
    name = args[0]
    book.delete(name)
    return f"{Fore.GREEN}Contact has been deleted."


@change_phone_validator
@base_input_validator
def change_phone(args, book: AddressBook):
    """
    Змінює номер телефону контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я, старий та новий номер телефону.

    Returns:
        str: Повідомлення про успішну зміну номера телефону.
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    if record.find_phone(old_phone) is None:
        return f"{Fore.RED}No such phone."
    record.edit_phone(old_phone, new_phone)
    return f"{Fore.GREEN}Phone has been changed."


@add_birthday_validator
@base_input_validator
def add_birthday(args, book: AddressBook):
    """
    Додає день народження до контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я та день народження.

    Returns:
        str: Повідомлення про успішне додавання дня народження.
    """
    name, birthday = args
    book.find(name).add_birthday(birthday)
    return f"{Fore.GREEN}Birthday has been added."


@base_input_validator
def show_birthday(args, book: AddressBook):
    """
    Показує день народження контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я контакту.

    Returns:
        str: День народження або повідомлення про його відсутність.
    """
    name = args[0]
    birthday = book.find(name).birthday
    return f"{Fore.YELLOW}{str(birthday)}" if birthday is not None else f"{Fore.RED}No birthday info."


@add_email_validator
@base_input_validator
def add_email(args, book: AddressBook):
    """
    Додає електронну адресу до контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я та електронну адресу.

    Returns:
        str: Повідомлення про успішне додавання електронної адреси.
    """
    name, email = args
    book.find(name).add_email(email)
    return f"{Fore.GREEN}Email has been added."


@change_email_validator
@base_input_validator
def change_email(args, book: AddressBook):
    """
    Змінює електронну адресу контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я, стару та нову електронну адресу.

    Returns:
        str: Повідомлення про успішну зміну елект
    """
    name, old_email, new_email = args
    record = book.find(name)
    if (record.find_email(old_email) is None):
        return f"{Fore.RED}No such email."
    record.change_email(old_email, new_email)
    return f"{Fore.GREEN}Email has been changed."


@base_input_validator
def show_email(args, book: AddressBook):
    """
    Показує електронну адресу контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я контакту.

    Returns:
        str: Електронна адреса або повідомлення про її відсутність.
    """
    name = args[0]
    emails = book.find(name).emails
    return f"{Fore.YELLOW}{'; '.join(email.value for email in emails)}" if len(emails) > 0 else f"{Fore.RED}No email."


@add_address_validator
@base_input_validator
def add_address(args, book: AddressBook):
    """
    Додає адресу до контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я та адресу.

    Returns:
        str: Повідомлення про успішне додавання адреси.
    """
    name, *address_parts = args
    record = book.find(name)
    had_address = record.address is not None

    # concatenate everything after name
    address = ' '.join(address_parts)
    record.add_address(address)

    return f"{Fore.GREEN}Address has been changed." if had_address else f"{Fore.GREEN}Address has been added."


@base_input_validator
def show_address(args, book: AddressBook):
    """
    Показує адресу контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я контакту.

    Returns:
        str: Адреса або повідомлення про її відсутність.
    """
    name = args[0]
    record = book.find(name)
    address = record.address
    return f"{Fore.YELLOW}{str(address)}" if address is not None else f"{Fore.RED}No address found."


@base_input_validator
def show_phones(args, book: AddressBook):
    """
    Показує номери телефонів контакту.

    Args:
        args (list): Список аргументів, включаючи ім'я контакту.

    Returns:
        str: Номери телефонів.
    """
    name = args[0]
    phones = book.find(name).phones
    return f"{Fore.YELLOW}{'; '.join(phone.value for phone in phones)}"


@find_contact_validator
def find_contact(args, book: AddressBook):
    """
    Знаходить контакт за заданим словом.

    Args:
        args (list): Список аргументів, включаючи слово для пошуку.

    Returns:
        str: Знайдений контакт або повідомлення про відсутність результатів.
    """
    search_word = args[0]
    result = book.search_contacts(search_word)

    if not result:
        return "No result."
    else:
        return '\n'.join(f"{Fore.YELLOW}{str(record)}" for record in result)


@base_input_validator
def show_all(book: AddressBook):
    """
    Виводить всі контакти з адресної книги.

    Args:
    book (AddressBook): Екземпляр класу AddressBook, який містить контакти.

    Returns:
    str: Рядок з усіма контактами або повідомлення про їх відсутність.
    """
    if (len(book) == 0):
        return "No contacts."
    else:
        return '\n'.join(f"{Fore.YELLOW}{str(record)}" for record in book.values())


@birthdays_input_validator
@base_input_validator
def birthdays(args, book: AddressBook):
    """
    Виводить контакти, у яких день народження протягом заданої кількості днів.

    Args:
    args (list): Список аргументів, де перший елемент може бути кількістю днів для перевірки.
    book (AddressBook): Екземпляр класу AddressBook, який містить контакти.

    Returns:
    str: Рядок з контактами, у яких день народження протягом заданої кількості днів.
    """
    if (len(book) == 0):
        return f"{Fore.RED}No contacts."
    else:
        # one week by default
        days_count = 7
        if (len(args) > 0):
            days_count = int(args[0])
        return f"{Fore.YELLOW}Birthdays during {days_count} day(s)\n" + book.get_birthdays_per_week(days_count)

def get_unique_cleaned_non_empty_tags(input_tags: str):
    """
    Повертає унікальні, очищені від зайвих пробілів та лапок теги.

    Args:
        input_tags (str): Рядок тегів, розділених комами.

    Returns:
        list: Список унікальних тегів.
    """
    cleaned_tags = [tag.strip().strip('\'\"') for tag in input_tags.split(',')]
    return list(set(cleaned_tags))

def get_note_property(msg):
    """
    Отримує властивість нотатки від користувача.

    Args:
        msg (str): Повідомлення для користувача.

    Returns:
        str: Введена властивість.
    """
    while True:
        input_value = input(f"{Fore.BLUE}{msg}")
        if input_value.strip() == 'exit':
            break
        elif input_value.strip() == '':
            print(f"{Fore.RED}Value cannot be empty.")
        else:
            return input_value

@note_error
def add_note(args, book: NotesBook):
    """
    Додає нотатку до блокноту.

    Args:
        args (list): Список аргументів, включаючи заголовок нотатки.

    Returns:
        str: Повідомлення про успішне додавання нотатки.
    """
    title = " ".join(args)
    if (title == ''):
        title = get_note_property("Enter note title: ")
    if (title == ''):
        return f"{Fore.RED}Note is not created."

    description = get_note_property("Enter note description: ")

    input_tags = input(f"{Fore.BLUE}Enter note tags separated by commas: ")

    cleaned_tags = get_unique_cleaned_non_empty_tags(input_tags)

    note = Note(title)
    note.description = description
    note.tags = cleaned_tags
    book.add_note(note)
    return f"{Fore.GREEN}Note '{title}' has been added."


@note_error
def delete_note(args, book: NotesBook):
    """
    Видаляє нотатку з блокноту.

    Args:
        args (list): Список аргументів, включаючи заголовок нотатки.

    Returns:
        str: Повідомлення про успішне видалення нотатки.
    """
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        book.delete_note(note)
        return f"{Fore.GREEN}Note '{title}' has been successfully deleted."
    else:
        return f"{Fore.RED}Note '{title}' has not been found."


@note_error
def change_note(args, book: NotesBook):
    """
    Змінює нотатку в блокноті.

    Args:
        args (list): Список аргументів, включаючи заголовок нотатки.

    Returns:
        str: Повідомлення про успішну зміну нотатки.
    """
    title = " ".join(args)
    note = book.find_note_by_title(title)

    if note is not None:
        new_description = input(f"{Fore.BLUE}Enter note description please: ")
        if new_description.strip() == "":
            new_description = note.description.value

        new_tags_input = input(f"{Fore.BLUE}Enter note tags separated by commas please: ")
        if new_tags_input.strip() == "":
            new_tags = note.tags
        else:
            new_tags = get_unique_cleaned_non_empty_tags(new_tags_input)
        book.edit_note(note, title=None, description=new_description, tags=new_tags)
        return f"{Fore.GREEN}Note '{note.title}' has been successfully changed."
    else:
        return f"{Fore.RED}Note with title '{title}' was not found."

@note_error
def show_all_notes(book: NotesBook):
    """
    Показує всі нотатки.

    Args:
        book (NotesBook): Блокнот з нотатками.

    Returns:
        str: Всі нотатки або повідомлення про їх відсутність.
    """
    book.print_all_notes()


@note_error
def show_note(args, book: NotesBook):
    """
    Показує нотатку за заголовком.

    Args:
        args (list): Список аргументів, включаючи заголовок нотатки.

    Returns:
        str: Нотатка або повідомлення про її відсутність.
    """
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        return note
    else:
        return f"{Fore.RED}Note '{title}' has not been found."


@note_error
def add_tags(args, book: NotesBook):
    """
    Додає теги до нотатки.

    Args:
        args (list): Список аргументів, включаючи заголовок нотатки.

    Returns:
        str: Повідомлення про успішне додавання тегів.
    """
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        tags = input(f"{Fore.BLUE}Enter note tags separated by commas pleas: ")
        cleaned_tags = get_unique_cleaned_non_empty_tags(tags)

        note.add_tags(set(cleaned_tags))
        msg = f"{Fore.GREEN}Tags {cleaned_tags} of note '{title}' have been added."
        if (len(cleaned_tags) == 1 and cleaned_tags[0] == ''):
            msg = f"{Fore.RED}Tags can't be empty."
        return msg
    else:
        return f"{Fore.RED}Note '{title}' has not been not found."


@note_error
def delete_tags(args, book: NotesBook):
    """
    Видаляє теги з нотатки у NotesBook.

    Args:
        args (list): Список аргументів, де перший елемент очікується як назва нотатки.
        book (NotesBook): Екземпляр класу NotesBook.

    Returns:
        str: Повідомлення, що вказує результат операції.
    """
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        tags = input(f"{Fore.BLUE}Enter note tags for deleting separated by commas pleas: ")
        cleaned_tags = get_unique_cleaned_non_empty_tags(tags)

        note.delete_tags(cleaned_tags)
        return f"{Fore.GREEN}Tags {tags} from note '{title}' have been deleted."
    else:
        return f"{Fore.RED}Note '{title}' has not been not found."


@note_error
def search_tags(args, book: NotesBook):
    """
    Шукає нотатки за тегами у NotesBook.

    Args:
        args (list): Список тегів для пошуку.
        book (NotesBook): Екземпляр класу NotesBook.

    Returns:
        None
    """
    tags = args
    notes = book.find_notes_by_tags(tags)
    if (notes is not None):
        book.print_notes(notes)
    else:
        print(f"{Fore.RED}No notes with tags '{tags}' have been found.")


def load_from_file():
    """
    Завантажує адресну книгу та книгу нотаток з файлу.

    Returns:
        tuple: Кортеж, що містить екземпляри AddressBook та NotesBook, завантажені з файлу.
    """
    try:
        with open('address_book.pkl', 'rb') as f:
            address_book = pickle.load(f)
        with open('notes_book.pkl', 'rb') as f:
            notes_book = pickle.load(f)
    except:
        address_book = AddressBook()
        notes_book = NotesBook()

    return address_book, notes_book


def save_to_file(address_book, notes_book):
    """
    Зберігає адресну книгу та книгу нотаток у файл.

    Args:
        address_book (AddressBook): Екземпляр класу AddressBook.
        notes_book (NotesBook): Екземпляр класу NotesBook.

    Returns:
        None
    """
    with open('address_book.pkl', 'wb') as f:
        pickle.dump(address_book, f)
    with open('notes_book.pkl', 'wb') as f:
        pickle.dump(notes_book, f)

def print_all_commands():
    """ Друкує список команд та їх пояснення. """
    commands = {
        f"- add-address {Fore.LIGHTYELLOW_EX}[name] [address]:": "Add an address, including country, city, street, and additional details.",
        f"- add-birthday {Fore.LIGHTYELLOW_EX}[name] [birthdate]:": "Add the birthdate for the specified contact.",
        f"- add {Fore.LIGHTYELLOW_EX}[name] [phone]:": "Add a new contact with name and phone number.",
        f"- add-email {Fore.LIGHTYELLOW_EX}[name] [email]:": "Add an email to the specified contact.",
        f"- add-note {Fore.LIGHTYELLOW_EX}[title]...[add description]...[add tags]:": "Add a title, then add a description and tags using the terminal prompt.",
        f"- add-tags {Fore.LIGHTYELLOW_EX}[title] ... [tags]:": "Add tags to a note using the terminal prompt.",
        f"- birthdays {Fore.LIGHTYELLOW_EX}[days number]:": "Show birthdays that will occur within the specified number of days.",
        f"- change-address {Fore.LIGHTYELLOW_EX}[name] [address]:": "Change the address for the specified contact.",
        f"- change-email {Fore.LIGHTYELLOW_EX}[name] [old email] [new email]:": "Change the email address for the specified contact from the old one to the new one.",
        f"- change-phone {Fore.LIGHTYELLOW_EX}[name] [old phone] [new phone]:": "Change the phone number for the specified contact from the old one to the new one.",
        f"- change-note {Fore.LIGHTYELLOW_EX}[title]...[description]...[tags]:": "Change description and tags using terminal prompt.",
        f"- delete-contact {Fore.LIGHTYELLOW_EX}[name]:": "Delete the entire contact record.",
        f"- delete-note {Fore.LIGHTYELLOW_EX}[title]:": "Delete the note.",
        f"- delete-tags {Fore.LIGHTYELLOW_EX}[title] ... [tags]:": "Delete the tag.",
        f"- find-contact {Fore.LIGHTYELLOW_EX}[param]:": "Display all contact records found by the specified parameter.",
        f"- phone {Fore.LIGHTYELLOW_EX}[name]:": "Show the phone number for the specified contact.",
        f"- search-tags {Fore.LIGHTYELLOW_EX}[tags]:": "Search notes by tags.",
        f"- show-address {Fore.LIGHTYELLOW_EX}[name]:": "Show the address for the specified contact.",
        f"- show-birthday {Fore.LIGHTYELLOW_EX}[name]:": "Show the birthdate for the specified contact.",
        f"- show-email {Fore.LIGHTYELLOW_EX}[name]:": "Show the email for the specified contact.",
        f"- show-note {Fore.LIGHTYELLOW_EX}[title]:": "Show a note."
    }

    commands_without_params = {
    "- all:": "Show all contacts in the address book.",
    "- all-notes:": "Show all notes.",
    "- birthdays:": "Show birthdays that will occur within 7 days.",
    "- close or exit:": "Close the application.",
    "- hello:": "Show text 'How can I help you?'"}

    print(Fore.BLUE + "COMMAND LIST:")
    for command, description in commands.items():
        print(f"{Fore.LIGHTGREEN_EX}{command:<58} {Fore.WHITE}{'|':^1} {Fore.LIGHTBLUE_EX} {description}")

    for command, description in commands_without_params.items():
        print(f"{Fore.LIGHTGREEN_EX}{command:<53} {Fore.WHITE}{'|':^1} {Fore.LIGHTBLUE_EX} {description}")


def handle_command(command, args, address_book, notes_book):
    """
    Обробляє команди користувача та виконує відповідні дії з адресною книгою та книгою нотаток.

    Args:
        command (str): Команда, яку потрібно виконати.
        args (list): Список аргументів, які передаються разом з командою.
        address_book (AddressBook): Екземпляр класу AddressBook, який містить контакти.
        notes_book (NotesBook): Екземпляр класу NotesBook, який містить нотатки.

    Returns:
        None
    """
    if command == "hello":
        print(Fore.BLUE + "How can I help you?")
    elif command == "add":
        print(add_contact(args, address_book))
    elif command == "delete-contact":
        print(delete_contact(args, address_book))
    elif command == "change-phone":
        print(change_phone(args, address_book))
    elif command == "add-birthday":
        print(add_birthday(args, address_book))
    elif command == "show-birthday":
        print(show_birthday(args, address_book))
    elif command == "add-email":
        print(add_email(args, address_book))
    elif command == "show-email":
        print(show_email(args, address_book))
    elif command == "change-email":
        print(change_email(args, address_book))
    elif command in ["add-address", "change-address"]:
        print(add_address(args, address_book))
    elif command == "show-address":
        print(show_address(args, address_book))
    elif command == "phone":
        print(show_phones(args, address_book))
    elif command == "find-contact":
        print(find_contact(args, address_book))
    elif command == "all":
        print(show_all(address_book))
    elif command == "birthdays":
        print(birthdays(args, address_book))
    elif command == "add-note":
        print(add_note(args, notes_book))
    elif command == "change-note":
        print(change_note(args, notes_book))
    elif command == "show-note":
        print(show_note(args, notes_book))
    elif command == "add-tags":
        print(add_tags(args, notes_book))
    elif command == "delete-tags":
        print(delete_tags(args, notes_book))
    elif command == "search-tags":
        search_tags(args, notes_book)
    elif command == "delete-note":
        print(delete_note(args, notes_book))
    elif command == "all-notes":
        show_all_notes(notes_book)
    else:
        print(Fore.RED + "Invalid command.")


def main():
    """
    Головна функція, яка запускає бот-асистент.

    Завантажує дані з файлів, виводить привітання та перевіряє наявність днів народження.
    Запускає цикл обробки команд користувача до тих пір, поки не буде введено команду для виходу.
    Після завершення роботи зберігає дані у файли.

    Args:
        None

    Returns:
        None
    """
    address_book, notes_book = load_from_file()

    print(f"{Fore.BLUE}Welcome to the assistant bot!")
    birthdays_today = address_book.today_birthdays()
    if birthdays_today:
        names = ", ".join(birthdays_today)
        print(f"{Fore.MAGENTA}Greetings! There are birthdays in your Address Book today!\nDo not forget to congratulate {names}!")
    print_all_commands()

    command_list = WordCompleter([
    'add-address', 'add-birthday', 'add', 'add-email', 'add-note', 'add-tags', 'all', 'all-notes',
    'birthdays', 'close', 'exit', 'change-address', 'change-email', 'change-phone', 'change-note',
    'delete-contact', 'delete-note', 'delete-tags', 'find-contact', 'hello', 'phone', 'search-tags',
    'show-address', 'show-birthday', 'show-email', 'show-note'])

    while True:
        user_input = prompt('Enter a command: ', completer=command_list)
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_to_file(address_book, notes_book)
            print(Fore.BLUE + "Good bye!")
            break
        else:
            handle_command(command, args, address_book, notes_book)


if __name__ == "__main__":
    main()
