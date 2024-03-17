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
    if len(user_input) > 0:
        cmd, *args = user_input.split()
    else:
        cmd, *args = '', []
    cmd = cmd.strip().lower()
    return cmd, *args


def note_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)

    return inner


def base_input_validator(func):
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
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and phone please."

    return inner


def change_phone_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name, old phone and new phone please."

    return inner


def add_birthday_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and birthday please."

    return inner


def birthdays_input_validator(func):
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
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name and email please."

    return inner


def change_email_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"{Fore.BLUE}Give me name, old email and new email please."

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
            return f"{Fore.BLUE}Give me name and address please."

    return inner


def find_contact_validator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return f"{Fore.BLUE}Give me search word please."

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
    return f"{Fore.GREEN}Contact has been added."


@base_input_validator
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return f"{Fore.GREEN}Contact has been deleted."


@change_phone_validator
@base_input_validator
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record.find_phone(old_phone) is None:
        return f"{Fore.RED}No such phone."
    record.edit_phone(old_phone, new_phone)
    return f"{Fore.GREEN}Phone has been changed."


@add_birthday_validator
@base_input_validator
def add_birthday(args, book: AddressBook):
    name, birthday = args
    book.find(name).add_birthday(birthday)
    return f"{Fore.GREEN}Birthday has been added."


@base_input_validator
def show_birthday(args, book: AddressBook):
    name = args[0]
    birthday = book.find(name).birthday
    return f"{Fore.YELLOW}{str(birthday)}" if birthday is not None else f"{Fore.RED}No birthday info."


@add_email_validator
@base_input_validator
def add_email(args, book: AddressBook):
    name, email = args
    book.find(name).add_email(email)
    return f"{Fore.GREEN}Email has been added."


@change_email_validator
@base_input_validator
def change_email(args, book: AddressBook):
    name, old_email, new_email = args
    record = book.find(name)
    if (record.find_email(old_email) is None):
        return f"{Fore.RED}No such email."
    record.change_email(old_email, new_email)
    return f"{Fore.GREEN}Email has been changed."


@base_input_validator
def show_email(args, book: AddressBook):
    name = args[0]
    emails = book.find(name).emails
    return f"{Fore.YELLOW}{'; '.join(email.value for email in emails)}" if len(emails) > 0 else f"{Fore.RED}No email."


@add_address_validator
@base_input_validator
def add_address(args, book: AddressBook):
    name, *address_parts = args
    record = book.find(name)
    had_address = record.address is not None

    # concatenate everything after name
    address = ' '.join(address_parts)
    record.add_address(address)

    return f"{Fore.GREEN}Address has been changed." if had_address else f"{Fore.GREEN}Address has been added."


@base_input_validator
def show_address(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    address = record.address
    return f"{Fore.YELLOW}{str(address)}" if address is not None else f"{Fore.RED}No address found."


@base_input_validator
def show_phones(args, book: AddressBook):
    name = args[0]
    phones = book.find(name).phones
    return f"{Fore.YELLOW}{'; '.join(phone.value for phone in phones)}"


@find_contact_validator
def find_contact(args, book: AddressBook):
    search_word = args[0]
    result = book.search_contacts(search_word)

    if not result:
        return "No result."
    else:
        return '\n'.join(f"{Fore.YELLOW}{str(record)}" for record in result)


@base_input_validator
def show_all(book: AddressBook):
    if (len(book) == 0):
        return "No contacts."
    else:
        return '\n'.join(f"{Fore.YELLOW}{str(record)}" for record in book.values())


@birthdays_input_validator
@base_input_validator
def birthdays(args, book: AddressBook):
    if (len(book) == 0):
        return f"{Fore.RED}No contacts."
    else:
        # one week by default
        days_count = 7
        if (len(args) > 0):
            days_count = int(args[0])
        return f"{Fore.YELLOW}Birthdays during {days_count} day(s)\n" + book.get_birthdays_per_week(days_count)

def get_unique_cleaned_non_empty_tags(input_tags: str):
    cleaned_tags = [tag.strip().strip('\'\"') for tag in input_tags.split(',')]
    return list(set(cleaned_tags))

def get_note_property(msg):
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
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        book.delete_note(note)
        return f"{Fore.GREEN}Note '{title}' has been successfully deleted."
    else:
        return f"{Fore.RED}Note '{title}' has not been found."


@note_error
def change_note(args, book: NotesBook):
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


@note_error
def show_all_notes(book: NotesBook):
    book.print_all_notes()


@note_error
def show_note(args, book: NotesBook):
    title = " ".join(args)
    note = book.find_note_by_title(title)
    if (note is not None):
        return note
    else:
        return f"{Fore.RED}Note '{title}' has not been found."


@note_error
def add_tags(args, book: NotesBook):
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
    tags = args
    notes = book.find_notes_by_tags(tags)
    if (notes is not None):
        book.print_notes(notes)
    else:
        print(f"{Fore.RED}No notes with tags '{tags}' have been found.")


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


def print_all_commands():
    print("Command list:")
    print(f"{Fore.LIGHTGREEN_EX}- add-address {Fore.LIGHTYELLOW_EX}[name] [address]:                {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add an address, str. etc")
    print(f"{Fore.LIGHTGREEN_EX}- add-birthday {Fore.LIGHTYELLOW_EX}[name] [birthdate]:             {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add the birthdate for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- add {Fore.LIGHTYELLOW_EX}[name] [phone]:                          {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add a new contact with name and phone number.")
    print(f"{Fore.LIGHTGREEN_EX}- add-email {Fore.LIGHTYELLOW_EX}[name] [email]:                    {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add an email to the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- add-note {Fore.LIGHTYELLOW_EX}[title] [text]:                     {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add a note.")
    print(f"{Fore.LIGHTGREEN_EX}- add-tags {Fore.LIGHTYELLOW_EX}[title][tag]...[tag]:               {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Add a tag(s) to the note.")
    print(f"{Fore.LIGHTGREEN_EX}- all:                                         {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show all contacts in the address book.")
    print(f"{Fore.LIGHTGREEN_EX}- all-notes:                                   {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show all notes.")
    print(f"{Fore.LIGHTGREEN_EX}- birthdays:                                   {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show birthdays that will occur within 7 days.")
    print(f"{Fore.LIGHTGREEN_EX}- birthdays {Fore.LIGHTYELLOW_EX}[days number]:                     {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show birthdays that will occur within the specified number of days.")
    print(f"{Fore.LIGHTGREEN_EX}- close or exit:                               {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Close the application.")
    print(f"{Fore.LIGHTGREEN_EX}- change-address {Fore.LIGHTYELLOW_EX}[name] [address]:             {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Change the address for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- change-email {Fore.LIGHTYELLOW_EX}[name] [old email] [new email]: {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Change the email for the specified contact by adding from the old email to the new one.")
    print(f"{Fore.LIGHTGREEN_EX}- change-phone {Fore.LIGHTYELLOW_EX}[name] [old phone] [new phone]: {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Change the phone number for the specified contact, transferring from the old to the new.")
    print(f"{Fore.LIGHTGREEN_EX}- change-note {Fore.LIGHTYELLOW_EX}[title] [text]:                  {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Change a note.")
    print(f"{Fore.LIGHTGREEN_EX}- delete-contact {Fore.LIGHTYELLOW_EX}[name]:                       {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Delete the entire contact record.")
    print(f"{Fore.LIGHTGREEN_EX}- delete-note {Fore.LIGHTYELLOW_EX}[title]:                         {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Delete the note")
    print(f"{Fore.LIGHTGREEN_EX}- delete-tags {Fore.LIGHTYELLOW_EX}[tag]:                           {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Delete the tag.")
    print(f"{Fore.LIGHTGREEN_EX}- find-contact {Fore.LIGHTYELLOW_EX}[param]:                        {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Display all contact records found by the specified parameter.")
    print(f"{Fore.LIGHTGREEN_EX}- hello:                                       {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show text 'How can I help you?'")
    print(f"{Fore.LIGHTGREEN_EX}- phone {Fore.LIGHTYELLOW_EX}[name]:                                {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show the phone number for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- search-tag {Fore.LIGHTYELLOW_EX}[tag]:                            {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show notes by tag.")
    print(f"{Fore.LIGHTGREEN_EX}- show-address {Fore.LIGHTYELLOW_EX}[name]:                         {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show the address for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- show-birthday {Fore.LIGHTYELLOW_EX}[name]:                        {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show the birthdate for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- show-email {Fore.LIGHTYELLOW_EX}[name]:                           {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show the email for the specified contact.")
    print(f"{Fore.LIGHTGREEN_EX}- show-note {Fore.LIGHTYELLOW_EX}[title]:                           {Fore.WHITE}| {Fore.LIGHTBLUE_EX}Show a note.")
    

def handle_command(command, args, address_book, notes_book):
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
    address_book, notes_book = load_from_file()

    print("Welcome to the assistant bot!")
    birthdays_today = address_book.today_birthdays()
    if birthdays_today:
        names = ", ".join(birthdays_today)
        print(f"Greetings! There are birthdays in your Address Book today!\nDo not forget to congratulate {names}!")
    print_all_commands()

    command_list = WordCompleter([
    'add-address', 'add-birthday', 'add', 'add-email', 'add-note', 'add-tags', 'all', 'all-notes',
    'birthdays', 'close', 'exit', 'change-address', 'change-email', 'change-phone', 'change-note',
    'delete-contact', 'delete-note', 'delete-tags', 'find-contact', 'hello', 'phone', 'search-tag',
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
