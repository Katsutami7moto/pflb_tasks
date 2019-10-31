import os
import sys


def load_data(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ''
    with open(filepath, encoding='utf-8') as handle:
        return handle.read()


def read_folder(folder_name: str) -> list:
    folder_files = []

    def get_file(n: int):
        return os.path.join(folder_name, 'Cash' + str(n + 1) + '.txt')
    for i in range(5):
        file = load_data(get_file(i))
        if not file:
            print('File of Cash {0} not found.\n'.format(i + 1))
            sys.exit(1)
        s_file = file.split('\n')
        folder_files.append(list(map(float, s_file)))
    return folder_files


def index_of_max(intervals: list) -> int:
    max_index, max_value = max(enumerate(intervals), key=lambda p: p[1])
    return max_index + 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong number of arguments.\n')
        sys.exit(1)
    cashiers = read_folder(sys.argv[1])
    store_intervals = [sum(x) for x in zip(*cashiers)]
    result = index_of_max(store_intervals)
    print(result)
