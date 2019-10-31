import os
import sys
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def points_are_equal(first: Point, second: Point) -> bool:
    return first.x == second.x and first.y == second.y


def load_data(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ''
    with open(filepath, encoding='utf-8') as handle:
        return handle.read()


def point_from_string(point: str) -> Point:
    return Point._make(map(float, point.split(' ')))


def list_of_points(loaded_data: str) -> list:
    point_strings = loaded_data.split('\n')
    return list(map(point_from_string, point_strings))


def locate_point(checking: Point, lines_first: Point, lines_second: Point, not_lines: Point) -> float:
    return ((not_lines.x - lines_first.x) * (lines_second.y - lines_first.y) - (not_lines.y - lines_first.y)
            * (lines_second.x - lines_first.x))\
           * ((checking.x - lines_first.x)
              * (lines_second.y - lines_first.y) - (checking.y - lines_first.y) * (lines_second.x - lines_first.x))


def check_point(checking: Point, quadrangle_points: list) -> int:
    if any(map(lambda p: points_are_equal(checking, p), quadrangle_points)):
        return 0
    check_sides = (
        locate_point(checking, quadrangle_points[0], quadrangle_points[1], quadrangle_points[2]),
        locate_point(checking, quadrangle_points[1], quadrangle_points[2], quadrangle_points[3]),
        locate_point(checking, quadrangle_points[2], quadrangle_points[3], quadrangle_points[0]),
        locate_point(checking, quadrangle_points[3], quadrangle_points[0], quadrangle_points[1])
    )
    if all(map(lambda s: s >= 0, check_sides)):
        if any(map(lambda s: s == 0, check_sides)):
            return 1
        else:
            return 2
    else:
        return 3


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Wrong number of arguments.\n')
        sys.exit(1)
    quadrangle_file_name = sys.argv[1]
    points_file_name = sys.argv[2]
    loaded_quadrangle = load_data(quadrangle_file_name)
    if not loaded_quadrangle:
        print('File of quadrangle not found.\n')
        sys.exit(1)
    loaded_points = load_data(points_file_name)
    if not loaded_points:
        print('File of points not found.\n')
        sys.exit(1)
    quadrangle = list_of_points(loaded_quadrangle)
    points_to_check = list_of_points(loaded_points)
    result = '\n'.join(map(lambda c: str(check_point(c, quadrangle)), points_to_check))
    print(result)
