'''Notes modul'''
import contextlib
import os.path
import pickle
import random
import time
from abc import ABC
from collections import UserDict
from datetime import datetime

from faker import Faker
from prettytable import NONE, PrettyTable
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from termcolor import colored, cprint

INVITATION = ' > '    # приглашение командной строки
MAX_STR_LEN = 50


class IntentCompleter(Completer):
    def __init__(self, commands):
        super().__init__()
        self.intents = commands

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        word_before_cursor = text_before_cursor.split()[-1] if text_before_cursor else ''

        for intent in self.intents:
            if intent.startswith(word_before_cursor):
                yield Completion(intent, start_position=-len(word_before_cursor))


class Field(ABC):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Notes(UserDict):
    filename = 'notes.sav'

    def add_note(self, note):
        note_id = self.new_id()
        note = Note(note, note_id)
        self.data[note.note_id] = note

    def new_id(self):
        if self.data:
            id_list = list(self.data.keys())
            id_list.sort()
            new_id = id_list[-1:][0] + 1
            return new_id
        else:
            return 1

    def find_in_notes(self, string):
        res = {}
        for k, v in self.data.items():
            if v.content.value.find(string.lower()) >= 0:
                res[k] = v
        return res

    def edit_note(self, note, note_id):
        self.data[note_id].edit_note(note)

    def del_note(self, note_id):
        self.data.pop(note_id)

    def add_tags(self, note_id, tags):
        if note_id in self.data.keys():
            self.data[note_id].add_note_tags(tags)

    def find_by_tag(self, string):
        res = {}
        for k, v in self.data.items():
            if v.tags.value:
                if string.lower() in v.tags.value:
                    res[k] = v
        return res

    def show_notes(self, data=None):
        l = MAX_STR_LEN
        if not data:
            data = self.data
        x = PrettyTable(align='l', header=False, vrules=NONE, max_table_width=l)
        for k, v in data.items():
            note = colored(v.content, 'blue') + '\n'
            if v.tags.value:
                note += colored(v.show_tags(), 'light_cyan') + '\n'
            dt = v.datetime.strftime("<%d-%m-%Y %H:%M>")
            note_id = 'id: ' + str(k)
            space = ' ' * (l - len(dt) - len(note_id) - 2)
            note += colored(dt + space + note_id, 'grey')
            x.add_row([note], divider=True)
        return x

    def iterator(self, step=5):
        data = list(self.data.values())
        while data:
            res = data[:step]
            data = data[step:]
            yield res

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
        return content


class Note:
    MAX_NOTE_LEN = 150   # max lenth of note

    def __init__(self, note, note_id):
        self.content = Content(note[:self.MAX_NOTE_LEN])
        self.tags = Tags()
        self.datetime = datetime.now()
        self.note_id = note_id

    def add_note_tags(self, tags):
        if not self.tags.value:
            self.tags.value = set()
        self.tags.value.update(tags.split())

    def del_tag(self, tag):
        if self.tags.value:
            self.tags.value.remove(tag)

    def show_tags(self):
        return '#' + ', #'.join(self.tags.value)

    def edit_note(self, new_text):
        self.content.value = new_text


class Content(Field):
    pass


class Tags(Field):
    def __init__(self, value=None):
        super().__init__(value)
        # self.value = value


def fake_notes(notes):
    fake = Faker(('uk_UA'))
    notes.add_note('Заметка о том, что нужно не забыть делать заметки,'
                   ' чтобы ничего не забывать :-)')
    time.sleep(0.1)
    for _ in range(10):
        i = random.randint(45, 210)
        notes.add_note(fake.text(i))
        time.sleep(0.1)


def show_greeting(commands):
    x = PrettyTable(align='l')
    x.field_names = [colored("Доступні команди:", 'light_blue')]
    for a, i in enumerate(commands, start=1):
        x.add_row([colored(f"{a}. {i}", "blue")])
    return x


def main():
    commands = ['add', 'show', 'find', 'edit', 'tag', 'tagfind', 'exit']
    session = PromptSession(auto_suggest=AutoSuggestFromHistory(),
                            completer=IntentCompleter(commands))

    notes = Notes()
    if not os.path.exists(notes.filename):
        fake_notes(notes)
    else:
        notes = notes.read_from_file()

    print(show_greeting(commands))

    while True:
        answer = session.prompt('Введіть команду' + INVITATION).strip()
        d, *args = answer.split(' ')
        with contextlib.suppress(ValueError):
            if int(d):
                for a, i in enumerate(commands, start=1):
                    if a == int(d):
                        d = i
        if answer == 'add' or d == 'add':     # добавление заметки
            note = input("Введіть свою нотатку" + INVITATION)
            if note:
                notes.add_note(note)
                notes.save_to_file()
                cprint("Вашу нотатку додано", 'green')
        elif answer == "show" or d == 'show':  # вывод всех заметок
            print(notes.show_notes())
        elif answer == "find" or d == 'find':  # поиск по заметкам
            string = input("Що знайти" + INVITATION)
            res = notes.find_in_notes(string)
            if res:
                print(notes.show_notes(res))
            else:
                cprint("Співпадінь не знайдено", 'green')
        elif answer == "edit" or d == 'edit':  # редактирование заметки
            note_id = int(input("Введіть id нотатки" + INVITATION))
            print(notes.show_notes({note_id: notes.data[note_id]}))
            note = input("Введіть новий текст" + INVITATION)
            notes.edit_note(note, note_id)
            notes.save_to_file()
            cprint("Нотатку змінено", 'green')
        elif answer == "tag" or d == 'tag':  # добавление тегов в заметку
            note_id = int(input("Введіть id нотатки" + INVITATION))
            print(notes.show_notes({note_id: notes.data[note_id]}))
            note = input("Введіть тег" + INVITATION)
            notes.add_tags(note_id, note)
            notes.save_to_file()
            cprint("Тег додано", 'green')
        elif answer == "tagfind" or d == 'tagfind':   # поиск по тегу
            string = input("Який тег знайти" + INVITATION)
            res = notes.find_by_tag(string)
            if res:
                print(notes.show_notes(res))
            else:
                cprint("Співпадінь не знайдено", 'green')
        elif answer == "del" or d == 'del':  # удаление заметки
            note_id = int(input("Введіть id нотатки" + INVITATION))
            notes.del_note(note_id)
            notes.save_to_file()
            cprint("Нотатку видалено", 'green')
        elif answer in ["exit", ""] or d == 'exit':    # выход из цикла
            notes.save_to_file()
            cprint('See you soon!', 'green')
            break


if __name__ == "__main__":
    main()
