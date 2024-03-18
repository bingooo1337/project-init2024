from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import re
from colorama import init, Fore

init()


class Field:
    """
    Клас Field визначає загальний тип для полів контакту.

    Атрибути:
        value (str): Значення поля.

    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас Name визначає поле для зберігання імені контакту.

    Аргументи:
        value (str): Значення поля.

    """

    def __init__(self, value):
        super().__init__(value)


class InvalidPhoneException(Exception):
    """Виключення, що виникає, коли номер телефону недійсний."""
    pass


class InvalidEmailException(Exception):
    """Виключення, що виникає, коли електронна адреса недійсна."""
    pass


def phone_validator(func):
    def inner(*args, **kwargs):
        if (len(args[1]) != 10):
            raise InvalidPhoneException
        return func(*args, **kwargs)

    return inner


def email_validator(func):
    def inner(*args, **kwargs):
        email = args[1]
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            raise InvalidEmailException
        return func(*args, **kwargs)

    return inner


class Phone(Field):
    """
    Клас Phone визначає поле для зберігання номера телефону контакту.

    Аргументи:
        value (str): Значення поля.

    """

    @phone_validator
    def __init__(self, value):
        super().__init__(value)


class Email(Field):
    """
    Клас Email визначає поле для зберігання електронної адреси контакту.

    Аргументи:
        value (str): Значення поля.

    """

    @email_validator
    def __init__(self, value):
        super().__init__(value)


class Address(Field):
    """
    Клас Address визначає поле для зберігання адреси контакту.

    Аргументи:
        value (str): Значення поля.

    """

    def __init__(self, value):
        super().__init__(value)


class InvalidBirthDateFormatException(Exception):
    """Виключення, що виникає, коли формат дати народження недійсний."""
    pass


def birthday_validator(func):
    def inner(*args, **kwargs):
        updated_args = list(args)
        try:
            updated_args[1] = datetime.strptime(
                args[1],
                Birthday.date_format,
            )
        except ValueError:
            raise InvalidBirthDateFormatException
        return func(*updated_args, **kwargs)

    return inner


class Birthday(Field):
    """
    Клас Birthday визначає поле для зберігання дати народження контакту.

    Атрибути:
        date_format (str): Формат дати.

    """

    date_format = "%d.%m.%Y"

    @birthday_validator
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return f"{Fore.YELLOW}{self.value.strftime(Birthday.date_format)}"


class Record:
    """
    Клас Record визначає контактну інформацію.

    Атрибути:
        name (Name): Ім'я контакту.
        phones (list): Список телефонних номерів.
        birthday (Birthday): Дата народження.
        emails (list): Список електронних адрес.
        address (Address): Адреса.

    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def add_phone(self, phone):
        """Додає новий номер телефону до контакту."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє вказаний номер телефону з контакту."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Змінює вказаний номер телефону на новий."""
        old = Phone(old_phone)
        for i, phone in enumerate(self.phones):
            if (phone.value == old.value):
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        """Знаходить телефонний номер."""
        find = Phone(phone)
        for p in self.phones:
            if (p.value == find.value):
                return p
        return None

    def add_email(self, email):
        """Додає нову електронну адресу до контакту."""
        self.emails.append(Email(email))

    def remove_email(self, email):
        """Видаляє вказану електронну адресу з контакту."""
        self.emails = [e for e in self.emails if e.value != email]

    def change_email(self, old_email, new_email):
        """Змінює вказану електронну адресу на нову."""
        old = Email(old_email)
        for i, email in enumerate(self.emails):
            if (email.value == old.value):
                self.emails[i] = Email(new_email)

    def find_email(self, email):
        """Знаходить електронну адресу."""
        find = Email(email)
        for e in self.emails:
            if (e.value == find.value):
                return e
        return None

    def add_birthday(self, birthday):
        """Додає дату народження контакту."""
        self.birthday = Birthday(birthday)

    def add_address(self, address):
        """Додає адресу контакту."""
        self.address = Address(address)

    def __str__(self):
        res = f"{Fore.YELLOW}Contact name: {self.name.value}; phones: {', '.join(p.value for p in self.phones)}"
        if (self.birthday is not None):
            res += f"; birthday: {self.birthday}"
        if (len(self.emails) > 0):
            res += f"; email(s): {', '.join(e.value for e in self.emails)}"
        if (self.address is not None):
            res += f"; address: {self.address}"
        return res


class AddressBook(UserDict):
    """
    Клас AddressBook визначає книгу контактів.

    Клас унаслідований від класу UserDict.

    """

    def add_record(self, record):
        """Додає новий запис до книги контактів."""
        self.data[record.name.value] = record

    def find(self, name):
        """Знаходить запис за іменем."""
        return self.data[name]

    def delete(self, name):
        """Видаляє запис за іменем."""
        del self.data[name]

    def search_contacts(self, search_word):
        """Шукає контакти за вказаним словом."""
        word = search_word.lower()
        results = []
        for record in self.values():
            # combine all info into one searchable line
            record_info = ' '.join([
                record.name.value,
                ' '.join(e.value for e in record.phones),
                ' '.join(e.value for e in record.emails),
                str(record.birthday) if record.birthday is not None else '',
                record.address.value if record.address is not None else '',
            ]).lower()

            if word in record_info:
                results.append(record)
        return results

    def get_birthdays_per_week(self, days_count: int):
        """Отримує дні народження за вказану кількість днів."""
        users_to_congratulate_by_days = self._get_users_to_congratulate(
            self.data.values(),
            days_count
        )

        lines = []
        for day in sorted(users_to_congratulate_by_days.items()):
            lines.append(f'{day[0].strftime("%A")}: {", ".join(day[1])}')

        return '\n'.join(lines)

    def _get_users_to_congratulate(self, users: list[Record], days_count: int):
        """Отримує користувачів, яких потрібно привітати."""
        start = datetime.now().date()
        end = (start + timedelta(days=days_count - 1))

        users_to_congratulate = defaultdict(list)
        for user in users:
            if (user.birthday is None):
                continue

            congratulation_day = self._get_congratulation_day(
                start,
                user.birthday.value.date()
            )

            if (start <= congratulation_day and congratulation_day <= end):
                users_to_congratulate[congratulation_day].append(
                    user.name.value
                )

        return users_to_congratulate

    def _get_congratulation_day(self, today, birthday):
        """Отримує день, коли потрібно привітати."""
        birthday_this_year = birthday.replace(year=today.year)

        congratulation_day = birthday_this_year

        # birthday will be next year
        if (birthday_this_year < today):
            congratulation_day = birthday_this_year.replace(
                year=today.year + 1)

        return congratulation_day
    
    def today_birthdays(self):
        """Отримує імена контактів, у яких сьогодні день народження."""
        today = datetime.now()
        birthdays_today = []

        for name in self:
            record = self.find(name)
            if record.birthday is not None and record.birthday.value.day == today.day and record.birthday.value.month == today.month:
                birthdays_today.append(name)
        return birthdays_today
