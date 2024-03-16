from notes_book import Note, NotesBook

note_1 = Note("Важливість води для організму")
note_1.description = "Важливість правильного харчування для здоров'я. Гідратація організму відіграє важливу роль у збереженні здоров'я."
note_1.tags = ["здоров'я", "харчування", "гідратація"]

note_2 = Note("Техніки концентрації під час навчання")
note_2.description = "Ефективні техніки концентрації, які допомагають під час навчання та роботи."
note_2.tags = ["освіта", "концентрація", "навчання"]

note_3 = Note("Секрети успішного управління часом")
note_3.description = "Ключові стратегії для ефективного управління часом та підвищення продуктивності."
note_3.tags = ["продуктивність", "управління часом", "організація"]

note_4 = Note("Переваги вегетаріанського харчування")
note_4.description = "Переваги вегетаріанського харчування для здоров'я та довголіття."
note_4.tags = ["здоров'я", "харчування", "вегетаріанство"]


notesBook = NotesBook()
notesBook.add_note(note_1)
notesBook.add_note(note_2)
notesBook.add_note(note_3)
notesBook.add_note(note_4)

print("print_all_notes:")
notesBook.print_all_notes()

print("add_tags:")
print(note_1.title)
note_1.add_tags("організм", "вода")
notesBook.print_notes([note_1])

print("delete_tags:")
# note_1.delete_tags("організм", "вода")
note_1.delete_tags(["організм", "вода"])
notesBook.print_notes([note_1])


print("find_note_by_title:")
print(notesBook.find_note_by_title("Важливість води для організму"))

print("find_notes_by_tags:")
notes = notesBook.find_notes_by_tags(["здоров'я", 'харчування'])
notesBook.print_notes(notes)

print("sort_notes_by_tags")
all_notes = notesBook.get_all_notes()
sorted_notes = notesBook.sort_notes_by_tags(all_notes, ["здоров'я", 'харчування'])
notesBook.print_notes(sorted_notes)

print("edite_note:")
note_to_edit = notesBook.find_note_by_title("Секрети успішного управління часом")
print(notesBook.edite_note(note_to_edit, title="Успішне управління часом", tags=['продуктивність', 'організація']))

print("delete_note:")
notesBook.delete_note(note_4)
notesBook.print_all_notes()