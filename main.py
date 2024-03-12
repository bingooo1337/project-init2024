import pickle
from address_book import AddressBook, InvalidBirthDateFormatException, InvalidPhoneException, Record


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such contact."
        except IndexError:
            return "Give me name please."
        except InvalidPhoneException:
            return "Phone number length should be 10."

    return inner


def change_contact_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name, old phone and new phone please."
        except KeyError:
            return "No such contact."
        except InvalidPhoneException:
            return "Phone number length should be 10."

    return inner


def add_birthday_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "No such contact."
        except ValueError:
            return "Give me name and birthday please."
        except InvalidBirthDateFormatException:
            return "Birthday should have format DD.MM.YYYY."

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args

    new_record = book.find(name)
    if (new_record == None):
        new_record = Record(name)

    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added."


@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return "Contact deleted."


@change_contact_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if (record.find_phone(old_phone) == None):
        return "No such phone."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@add_birthday_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    book.find(name).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    return str(book.find(name).birthday)


@input_error
def show_phones(args, book: AddressBook):
    name = args[0]
    phones = book.find(name).phones
    return '; '.join(phone.value for phone in phones)


@input_error
def show_all(book: AddressBook):
    if (len(book) == 0):
        return "No contacts."
    else:
        return '\n'.join(str(record) for record in book.values())


@input_error
def birthdays(book: AddressBook):
    if (len(book) == 0):
        return "No contacts."
    else:
        return book.get_birthdays_per_week()


def load_from_file():
    try:
        with open('address_book.pkl', 'rb') as f:
            book = pickle.load(f)
    except:
        book = AddressBook()

    return book


def save_to_file(book):
    with open('address_book.pkl', 'wb') as f:
        pickle.dump(book, f)


def main():
    book = load_from_file()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_to_file(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "phone":
            print(show_phones(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
