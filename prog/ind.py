import argparse
import pathlib
import json
import colorama
from colorama import Fore, Style
from typing import Union, List, Optional


def tree(directory: pathlib.Path) -> str:
    """
    Создание древа файлов
    """
    result_str = ""
    for path in sorted(directory.rglob("*")):
        depth = len(path.relative_to(directory).parts)
        spacer = " " * depth
        result_str += Fore.GREEN + Style.BRIGHT + f"{spacer} >> {path.name}\n"
        for new_path in sorted(directory.joinpath(path).glob("*")):
            depth = len(new_path.relative_to(directory.joinpath(path)).parts)
            spacer = "\t" * depth
            result_str += Fore.BLUE + f"{spacer} > {new_path.name}\n"
    return result_str


def size(filename: Union[str, pathlib.Path]) -> int:
    """
    Получение размера файла
    """
    file_stat = pathlib.Path(filename).stat()
    return file_stat.st_size


def save(filename: str, data: str) -> None:
    """
    Сохранить список самолетов в json-файл
    """
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(data, fout, ensure_ascii=False, indent=4)


def help() -> None:
    print("all - просмотр полного пути файла")
    print("files - просмотр всех файлов в директории")
    print("size - просмотр размера файла")
    print("save - сохранение данных в json-файл")
    print("mkdir - создание директории")
    print("rmdir - удаление директории")
    print("mk - создание файла")
    print("rm - удаление файла")


def main(command_line: Optional[List[str]] = None) -> None:
    colorama.init()
    current = pathlib.Path.cwd()
    file_parser = argparse.ArgumentParser(add_help=False)

    parser = argparse.ArgumentParser("tree")
    parser.add_argument(
        "--version", action="version", help="The main parser", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    create = subparsers.add_parser("mkdir", parents=[file_parser])
    create.add_argument("filename", action="store")

    create = subparsers.add_parser("rmdir", parents=[file_parser])
    create.add_argument("filename", action="store")

    create = subparsers.add_parser("mk", parents=[file_parser])
    create.add_argument("filename", action="store")

    create = subparsers.add_parser("rm", parents=[file_parser])
    create.add_argument("filename", action="store")

    create = subparsers.add_parser("help", parents=[file_parser])

    create = subparsers.add_parser("files", parents=[file_parser])

    create = subparsers.add_parser("size", parents=[file_parser])
    create.add_argument("filename", action="store")

    create = subparsers.add_parser("all", parents=[file_parser])

    create = subparsers.add_parser("save", parents=[file_parser])
    create.add_argument("filename", action="store")

    while True:
        user_input = input("Введите команду ('help' для списка команд): ")
        if user_input == "exit":
            break

        args = parser.parse_args(command_line or [])

        if args.command == "mkdir":
            directory_path = current / args.filename
            directory_path.mkdir()
        elif args.command == "rmdir":
            directory_path = current / args.filename
            directory_path.rmdir()
        elif args.command == "mk":
            directory_path = current / args.filename
            directory_path.touch()
        elif args.command == "rm":
            directory_path = current / args.filename
            directory_path.unlink()
        elif args.command == "all":
            print(Fore.RED + f"{current}")
        elif args.command == "help":
            help()
        elif args.command == "files":
            print(tree(current))
        elif args.command == "save":
            save(args.filename, tree(current))
        elif args.command == "size":
            directory_path = current / args.filename
            print(
                Fore.GREEN
                + Style.BRIGHT
                + f">> {args.filename}  -  {size(directory_path)} B"
            )
        else:
            print('Введите "help" для вывода списка команд')

        if args.command not in {"all", "help", "save", "size"}:
            print(tree(current))


if __name__ == "__main__":
    main()
