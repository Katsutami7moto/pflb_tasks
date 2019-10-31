import os
import sys


def load_data(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ''
    with open(filepath, encoding='utf-8') as handle:
        return handle.read()


def percentile(percentile_value: int, numbers: list) -> float:
    if len(numbers) == 1:
        return numbers[0]
    interval = 1.0 / (len(numbers) - 1)
    left_bound_index = int((percentile_value / 100.0) / interval)
    right_bound_index = left_bound_index if left_bound_index == len(numbers) - 1 else left_bound_index + 1
    return (((percentile_value / 100.0) - interval * left_bound_index) / interval) *\
           (numbers[right_bound_index] - numbers[left_bound_index]) + numbers[left_bound_index]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong number of arguments.\n')
        sys.exit(1)
    input_file_name = sys.argv[1]
    loaded_data = load_data(input_file_name)
    if not loaded_data:
        print('File not found.\n')
        sys.exit(1)
    data_to_calculate = list(map(int, loaded_data.split('\n')))
    perc = round(percentile(90, sorted(data_to_calculate)), 2)
    med = round(percentile(50, sorted(data_to_calculate)), 2)
    avg = round(sum(data_to_calculate) / len(data_to_calculate), 2)
    result = '{0:.2f}\n{1:.2f}\n{2:.2f}\n{3:.2f}\n{4:.2f}\n'\
        .format(perc, med, max(data_to_calculate), min(data_to_calculate), avg)
    print(result)
