import pickle
import re
from address_book import AddressBook, InvalidBirthDateFormatException, InvalidPhoneException, Record, InvalidEmailException, Email, Phone
from notes_book import NotesBook, Note


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def note_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)        
    return inner

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
        except InvalidEmailException:
            return "Please provide a valid email."


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
        except InvalidEmailException:
            return "Please provide a valid email."

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
def change_phone(args, book: AddressBook):
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
def add_email(args, book: AddressBook):
    name, email = args
    book.find(name).add_email(email)
    return "Email has been added."


@change_contact_error
def change_email(args, book:AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if (record.find_email(old_email) is None):
        return "No such email."
    record.change_email(old_email, new_email)
    return "Email has been changed."


@input_error
def show_email(args, book: AddressBook):
    name = args[0]
    emails = book.find(name).emails
    return '; '.join(email.value for email in emails)
    

def add_address(args, book: AddressBook):
    name, *address = args
    book.find(name).add_address(" ".join(address))
    return "Адреса додана."

def change_address(args, book: AddressBook):
    add_address(args, book)
    return ("Адреса змінена.")


@input_error
def show_address(args, book: AddressBook):
    name = args[0]
    return book.find(name).address


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
    # TODO add parameter with days length
    if (len(book) == 0):
        return "No contacts."
    else:
        return book.get_birthdays_per_week()


@note_error
def add_note(args, book: NotesBook):
    title = " ".join(args)
    description = input("Введіть опис нотатки: ")
    tags_input = input("Введіть теги нотатки через кому : ")
    
    cleaned_tags = [tag.strip().strip('\'\"') for tag in tags_input.split(',')]

    note = Note(title)
    note.description = description
    note.tags = cleaned_tags
    book.add_note(note)
    return f"Нотатка '{title}' створена."


@note_error
def delete_note(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        book.delete_note(note)
        return f"Нотатка '{title}' видалена."
    else:
        return f"Нотатка '{title}' не знайдена."


@note_error
def change_note(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    
    if note is not None:
        new_description = input("Введіть опис нотатки: ")
        if new_description.strip() == "":
            new_description = note.description

        new_tags_input = input("Введіть теги нотатки через кому: ")
        if new_tags_input.strip() == "":
            new_tags = note.tags
        else:
            new_tags = new_tags_input.split(r',\s*')

        book.edite_note(note, description=new_description, tags=new_tags)
        return f"Нотатка '{title}' змінена." 
    else:
        return f"Нотатка '{title}' не знайдена."

@note_error
def show_note(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        print(note)
    else:
        return f"Нотатка '{title}' не знайдена."

@note_error
def add_tags(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        tags = input("Введіть теги нотатки через кому : ").split(r',\s*')
        note.add_tags(*tags)
        return f"Теги {tags} до нотатки '{title}' додано."
    else:
        return f"Нотатка '{title}' не знайдена."

@note_error
def delete_tags(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        tags = input("Введіть теги для видалення через кому: ").split(',')
        cleaned_tags = [tag.strip('\'"') for tag in tags]
        note.delete_tags(cleaned_tags)
        return f"Теги {tags} з нотатки '{title}' видалено."
    else:
        return f"Нотатка '{title}' не знайдена."

@note_error
def search_tags(args, book: NotesBook):
    tags = args
    notes = book.find_notes_by_tags(tags)
    if (notes is not None):
        book.print_notes(notes)
    else:
        print(f"Нотатки з тегами '{tags}' не знайдено.")


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

def find_contacts(arg: str, book: AddressBook)-> list:
    pass


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
    elif command == "find-contact":
        print(find_contacts(args, address_book))
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
    elif command == "add-address":
        print(add_address(args, address_book))
    elif command == "change-address":
        print(change_address(args, address_book))
    elif command == "show-address":
        print(show_address(args, address_book))
    elif command == "phone":
        print(show_phones(args, address_book))
    elif command == "all":
        print(show_all(address_book))
    elif command == "birthdays":
        print(birthdays(address_book))
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
        notes_book.print_all_notes()
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
