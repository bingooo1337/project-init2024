from collections import UserDict
from address_book import Field
from colorama import init, Fore

init()


class Title(Field):
    def __init__(self, value):
        super().__init__(value)      

class Description(Field):
    def __init__(self, value):
        super().__init__(value)  

class Note:
    def __init__(self, title) -> None:
        self._title = Title(title)
        self._description = None
        self._tags = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title.value = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = Description(value)

    @property
    def tags(self):
        return self._unique_non_empty_tags(self._tags)

    @tags.setter
    def tags(self, value: list):
        self._tags = self._unique_non_empty_tags(value)

    def add_tags(self, tags: list):
        for tag in tags:
            self._tags.append(tag)

    def delete_tags(self, tags):
        for tag in tags:
            if tag in self._tags:
                self._tags.remove(tag)
            else:
                raise ValueError(f"{Fore.RED}Tag '{tag}' has not been not found.")
            
    def _unique_non_empty_tags(self, tags: list) -> list:
        non_empty_tags = [tag for tag in tags if tag != '']
        return list(set(non_empty_tags))
        
    def __repr__(self):
        head = "========================\n"
        return f"{Fore.WHITE}{head}{Fore.BLUE}title={self.title}\n{Fore.YELLOW}description={self.description if self.description else None}\ntags={self.tags}\n"


class NotesBook(UserDict):
    
    def add_note(self, note: Note):
        self.data[note.title.value] = note

    def edit_note(self, old_note: Note, title=None, description=None, tags=None) -> Note:
        if old_note.title.value in self.data:
            if title is not None:
                old_note.title.value = title
            if description is not None:
                old_note.description.value = description
            if tags is not None:
                old_note.tags = tags
            return old_note
        else:
            raise KeyError(f"{Fore.RED}Note with title '{old_note.title.value}' has not been not found.")

    def delete_note(self, note: Note):
        if note.title.value in self.data:
            del self.data[note.title.value]
        else:
            raise KeyError(f"{Fore.RED}Note '{note.title.value}' has not been not found.")

    def get_all_notes(self) -> list:
        return list(self.data.values())
    
    def print_notes(self, notes: list):
        for note in notes:
            print(note)
    
    def print_all_notes(self) -> None:
        self.print_notes(self.data.values())

    def find_note_by_title(self, title: str) -> Note:
        if title in self.data:
            return self.data[title]
        else:
            return None

    def find_notes_by_tags(self, tags: list) -> list:
        cleaned_tags = [tag.strip('\'"') for tag in tags]
        found_notes = []
        for note in self.data.values():
            if any(cleaned_tag in note.tags for cleaned_tag in cleaned_tags):
                found_notes.append(note)
        return found_notes

    def sort_notes_by_tags(self, notes, tags=None):
        if tags is not None:
           sorted_notes = sorted(notes, key=lambda note: any(tag in note.tags for tag in tags), reverse=True)
           return sorted_notes