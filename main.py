import argparse

from region_finder import RegionFinderWithSQLADB
from session import session


def parse_arguments() -> str:
    """Возвращает название переданного как параметр файла."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        help='путь до файла с входными данными')
    args = parser.parse_args()
    return args.filename


def main() -> None:
    """Точка входа в программу."""

    with open(parse_arguments(), 'r') as f, session:
        addresses = [strq.strip('\n') for strq in f.readlines()]
        for address in addresses:
            r = RegionFinderWithSQLADB(address, session=session)
            print(address, r.define_regions())


if __name__ == '__main__':
    main()
