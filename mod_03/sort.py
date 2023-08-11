import sys
import os
import shutil
from threading import Thread


EXT_DICT = {
            'IMAGES': ('JPEG', 'PNG', 'JPG', 'SVG'),
            'VIDEO': ('AVI', 'MP4', 'MOV', 'MKV'),
            'DOC': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
            'MUSIC': ('MP3', 'OGG', 'WAV', 'AMR'),
            'ARCHIVE': ('ZIP', 'GZ', 'TAR')
            }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i",
               "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
               "u", "f", "h", "ts", "ch", "sh", "sch", "", "y",
               "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

main_path = ''


def move_files_from_folders_on_top(path: str):
    for el in os.listdir(path):
        current = os.path.join(path, el)
        if os.path.isdir(current):
            thread = Thread(target=scan_folder, args=(current,))
            thread.start()
            delete_folder(current)


def scan_folder(path: str):
    print(path)
    for el in os.listdir(path):
        current = os.path.join(path, el)
        if os.path.isdir(current):
            scan_folder(current)
            delete_folder(current)
        else:
            move_file(current)


def move_file(file: str):
    print(os.path.split(file))
    if os.path.split(file)[0] != main_path:
        shutil.move(file, main_path)


def delete_folder(path: str):
    if len(os.listdir(path)) < 1:
        os.rmdir(path)


def move_by_order(path: str):
    for el in os.listdir(path):
        new_folder = find_destination_folder(el)
        if new_folder:
            new_name = normalise(el)
            old_file_path = os.path.join(path, el)
            new_path = os.path.join(path, new_folder)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            new_file_path = os.path.join(new_path, new_name)
            shutil.move(old_file_path, new_file_path)


def find_destination_folder(file):
    postfix = os.path.splitext(file)[1][1:].upper()
    for k, v in EXT_DICT.items():
        if postfix in v:
            return k
    return ''


def normalise(name: str) -> str:
    new_name = ''
    for n in name:
        if n.isalpha() or n.isdigit():
            new_name += n
        elif n == '.':
            new_name += n
        else:
            new_name += '_'
    return new_name.translate(TRANS)


def work_with_archive(path: str):
    for el in os.listdir(path):
        extract_folder = os.path.splitext(el)[0]
        extract_file = os.path.join(path, el)
        extract_path = os.path.join(path, extract_folder)
        if not os.path.exists(extract_path):
            os.mkdir(extract_path)
        shutil.unpack_archive(extract_file, extract_path)


def main() -> None:
    global main_path
    main_path = sys.argv[1]
    print(main_path)
    archive_path = os.path.join(main_path, 'ARCHIVE')

    move_files_from_folders_on_top(main_path)
    move_by_order(main_path)
    work_with_archive(archive_path)


if __name__ == "__main__":
    main()
