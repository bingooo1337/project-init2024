import pickle
from address_book import AddressBook, InvalidBirthDateFormatException, InvalidPhoneException, \
    Record, InvalidEmailException
from notes_book import NotesBook


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def base_input_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "No such contact."
        except IndexError:
            return "Give me name please."
        except InvalidPhoneException:
            return "Phone number length should be 10."
        except InvalidEmailException:
            return "Please provide a valid email."
        except InvalidBirthDateFormatException:
            return "Birthday should have format DD.MM.YYYY."

    return inner


def add_contact_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner


def change_contact_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name, old phone and new phone please."

    return inner


def add_birthday_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and birthday please."

    return inner


def birthdays_input_validator(func):
    def inner(*args, **kwargs):
        try:
            params = args[0]
            if (len(params) > 0):
                days_count = int(params[0])
                if (days_count < 1):
                    return "Give me the number of days > 0"

            return func(*args, **kwargs)
        except ValueError:
            return "Give me the number of days > 0"

    return inner


def add_address_validator(func):
    def inner(*args, **kwargs):
        try:
            # args after name
            address_parts = args[0][1:]
            if (len(address_parts) < 1):
                raise ValueError
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and address please."

    return inner


@add_contact_validator
@base_input_validator
def add_contact(args, book: AddressBook):
    name, phone = args

    try:
        new_record = book.find(name)
    except KeyError:
        new_record = Record(name)

    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added."


@base_input_validator
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return "Contact deleted."


@change_contact_validator
@base_input_validator
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record.find_phone(old_phone) is None:
        return "No such phone."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@add_birthday_validator
@base_input_validator
def add_birthday(args, book: AddressBook):
    name, birthday = args
    book.find(name).add_birthday(birthday)
    return "Birthday added."


@base_input_validator
def show_birthday(args, book: AddressBook):
    name = args[0]
    birthday = book.find(name).birthday
    return str(birthday) if birthday is not None else "No birthday info."


@base_input_validator
def add_email(args, book: AddressBook):
    name, email = args
    book.find(name).add_email(email)
    return "Email has been added."


@change_contact_validator
@base_input_validator
def change_email(args, book: AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if (record.find_email(old_email) is None):
        return "No such email."
    record.change_email(old_email, new_email)
    return "Email has been changed."


@base_input_validator
def show_email(args, book: AddressBook):
    name = args[0]
    emails = book.find(name).emails
    return '; '.join(email.value for email in emails)


@add_address_validator
@base_input_validator
def add_address(args, book: AddressBook):
    name, *address_parts = args
    record = book.find(name)
    had_address = record.address is not None

    # concatenate everything after name
    address = ' '.join(address_parts)
    record.add_address(address)

    return "Address changed." if had_address else "Address added."


@base_input_validator
def show_address(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    address = record.address
    return str(address) if address is not None else "No address."


@base_input_validator
def show_phones(args, book: AddressBook):
    name = args[0]
    phones = book.find(name).phones
    return '; '.join(phone.value for phone in phones)


@base_input_validator
def show_all(book: AddressBook):
    if (len(book) == 0):
        return "No contacts."
    else:
        return '\n'.join(str(record) for record in book.values())


@birthdays_input_validator
@base_input_validator
def birthdays(args, book: AddressBook):
    if (len(book) == 0):
        return "No contacts."
    else:
        # one week by default
        days_count = 7
        if (len(args) > 0):
            days_count = int(args[0])
        return f"Birthdays during {days_count} day(s)\n" + book.get_birthdays_per_week(days_count)


@base_input_validator
def add_note(args, book: NotesBook):
    # TODO
    return "Note added."


@base_input_validator
def delete_note(args, book: NotesBook):
    # TODO
    return 'Delete note'


@base_input_validator
def change_note(args, book: NotesBook):
    # TODO
    return "Note changed."


@base_input_validator
def show_all_notes(args, book: NotesBook):
    # TODO
    return 'All notes'


def load_from_file():
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
    with open('address_book.pkl', 'wb') as f:
        pickle.dump(address_book, f)
    with open('notes_book.pkl', 'wb') as f:
        pickle.dump(notes_book, f)


# TODO
def print_all_commands():
    print("all_commands")


def handle_command(command, args, address_book, notes_book):
    if command == "hello":
        print("How can I help you?")
    elif command == "add":
        print(add_contact(args, address_book))
    elif command == "delete":
        print(delete_contact(args, address_book))
    elif command == "change":
        print(change_contact(args, address_book))
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
    elif command == "all":
        print(show_all(address_book))
    elif command == "birthdays":
        print(birthdays(args, address_book))
    elif command == "add-note":
        print(add_note(args, notes_book))
    elif command == "change-note":
        print(change_note(args, notes_book))
    elif command == "delete-note":
        print(delete_note(args, notes_book))
    elif command == "all-notes":
        print(show_all_notes(args, notes_book))
    else:
        print("Invalid command.")


def main():
    address_book, notes_book = load_from_file()

    print("Welcome to the assistant bot!")
    print_all_commands()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_to_file(address_book, notes_book)
            print("Good bye!")
            break
        else:
            handle_command(command, args, address_book, notes_book)


if __name__ == "__main__":
    main()
