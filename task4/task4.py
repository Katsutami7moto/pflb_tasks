import os
import sys
from collections import namedtuple
from datetime import datetime, time

Period = namedtuple('Period', ['start', 'end', 'count'])
Move = namedtuple('Move', ['time', 'mode'])  # mode == 'start' or 'end'


def load_data(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ''
    with open(filepath, encoding='utf-8') as handle:
        return handle.read()


def period_from_tuple(t: tuple) -> Period:
    return Period(datetime.strptime(t[0], '%H:%M').time(), datetime.strptime(t[1], '%H:%M').time(), 1)


def make_periods(data: str) -> list:
    s_data = data.split('\n')
    s_s_data = map(lambda s: tuple(s.split(' ')), s_data)
    return list(map(period_from_tuple, s_s_data))


def make_moves(periods_list: list) -> list:
    moves_list = []
    for period in periods_list:
        moves_list.append(Move(period.start, 'start'))
        moves_list.append(Move(period.end, 'end'))
    return moves_list


def count_people(moves_list: list):
    start = time(0, 0)
    count = 0
    all_periods = []
    for move in moves_list:
        if move.mode == 'start':
            count += 1
            start = move.time
        if move.mode == 'end':
            all_periods.append(Period(start, move.time, count))
            count -= 1
    return all_periods


def sum_periods(periods_list: list) -> list:
    summarized_periods = []
    flag = False
    for i in range(1, len(periods_list)):
        if not flag:
            if periods_list[i].start == periods_list[i-1].end and periods_list[i].count == periods_list[i-1].count:
                summarized_periods.append(Period(periods_list[i-1].start, periods_list[i].end, periods_list[i].count))
                flag = True
            else:
                if i == 1:
                    summarized_periods.append(periods_list[0])
                summarized_periods.append(periods_list[i])
        else:
            summarized_periods.append(periods_list[i])
    if flag:
        return sum_periods(summarized_periods)
    else:
        return summarized_periods


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Wrong number of arguments.\n')
        sys.exit(1)
    input_file_name = sys.argv[1]
    loaded_data = load_data(input_file_name)
    if not loaded_data:
        print('File not found.\n')
        sys.exit(1)
    periods = sorted(make_periods(loaded_data), key=lambda p: p.start)
    moves = sorted(make_moves(periods), key=lambda m: (m.time, m.mode))
    s_periods = sum_periods(count_people(moves))
    max_count = max(map(lambda p: p.count, s_periods))
    max_periods = filter(lambda p: p.count == max_count, s_periods)
    for mp in max_periods:
        print('{0} {1}'.format(mp.start.strftime('%H:%M'), mp.end.strftime('%H:%M')))
