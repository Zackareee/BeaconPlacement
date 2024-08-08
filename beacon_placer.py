"""
This module provides utilities for equally distributing coordinates around a
centerpoint. These coordinates are integer coordinates, and are calculated to be
the closest to their angle as possible without sacrificing accuracy. 

It includes functions for comparing two points in 2d space, finding the distance
from a point to its nearest integer point, and finding coordinates along a
desired angle.

Functions:
    distance_between_two_points(c1, c2): Calculate distance between two points
    distance_to_centerpoint(x, y): Calculate the distance to the nearest
      integer coordinate given a float coordinate.
    x_generator(lower, upper, angle, step): Return a set of coordinates of a
      point given its angle.
    y_generator(lower, upper, angle, step): Return a set of coordinates of a
      point given its angle.
    custom_sort(item): Return values to sort distance from coordinate, followed
      by distance from origin.
    coordinate_placement(count, offset, minimum, maximum): Creates a set of
      coordinates around a centerpoint equally seperated by angle.
"""

from itertools import chain
from typing import List, Tuple, Union, Generator
from math import floor, ceil, sqrt, tan, radians, cos, sin

def distance_between_two_points(
  c1: List[float],
  c2: List[float]
  ) -> float:
  """
  Calculate distance between two points

  Args:
    c1 (List[float]): X and Y coordinates of a point.
    c2 (List[float]): X and Y coordinates of a point.
  Returns:
    float: Distance between c1 and c2 in 2d space.
  """
  x1, y1 = c1[0], c1[1]
  x2, y2 = c2[0], c2[1]
  return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def distance_to_centerpoint(
  x: float,
  y: float
  ) -> float:
  """
  Calculate the distance to the nearest integer coordinate given a float 
  coordinate.

  Args:
    x (float): x of Coordinate.
    y (float): y of Coordinate.
  Returns:
    List(Tuple[int, int]): Distance from integer coordinate, Distance 
    from [0,0] coordinate. 
  """
  if isinstance(x, int) and isinstance(y, int):
    return 0
  round_up_x = ceil(x)
  round_up_y = ceil(y)
  round_down_x = floor(x)
  round_down_y = floor(y)
  distance_tr = sqrt(((x - round_up_x) ** 2) + ((y - round_up_y) ** 2))
  distance_tl = sqrt(((x - round_down_x) ** 2) + ((y - round_up_y) ** 2))
  distance_bl = sqrt(((x - round_down_x) ** 2) + ((y - round_down_y) ** 2))
  distance_br = sqrt(((x - round_up_x) ** 2) + ((y - round_down_y) ** 2))
  return min(distance_tr, distance_bl, distance_tl, distance_br)

def x_generator(
  lower: int,
  upper: int,
  lower_bounds: int,
  upper_bounds: int,
  angle: float,
  step: int = 1,
  debug: bool = False,
  ) -> Generator[List[float], None, None]:
  """
  Return a set of coordinates of a point given its angle.

  Args:
    lower (int): Minimum radius a point can be at.
    upper (int): Maximum adius a point can be at.
    angle (float): Angle from 0,0 the point is along.
    step (int): Step size of the range.
  Returns:
    Generator[List[float], None, None]: X and Y coordinate.  
  """
  for x in range(lower, upper, step):
    y = angle * x
    distance = distance_between_two_points([0, 0], [x, y])
    if debug:
      print(distance)
    if distance < abs(upper_bounds) and distance > abs(lower_bounds):
      yield([x, angle * x])

def y_generator(
  lower: int,
  upper: int,
  lower_bounds: int,
  upper_bounds: int,
  angle: float,
  step: int = 1
  ) -> Generator[float, None, None]:
  """
  Return a set of coordinates of a point given its angle.

  Args:
    lower (int): Minimum radius a point can be at.
    upper (int): Maximum adius a point can be at.
    angle (float): Angle from 0,0 the point is along.
    step (int): Step size of the range.
  Returns:
    Generator[List[float], None, None]: X and Y coordinate.  
  """
  for y in range(lower, upper, step):
    if angle == 0:
      x = 0
    else:
      x = y / angle
    distance = distance_between_two_points([0, 0], [x, y])
    if distance < abs(upper_bounds) and distance > abs(lower_bounds):
      yield([x, y])

def coordinate_generator(
    lower_bounds: int,
    upper_bounds: int,
    angle_deg: float
    ) -> List[Generator[int, None, None]]:
  """
  Return a list of coordinates of a point given its angle.

  Args:
    lower_bounds (int): Minimum radius a point can be at.
    upper_bounds (int): Maximum adius a point can be at.
    angle_deg (float): Angle from 0,0 the point is along.
  Returns:
    List[Generator[int, None, None]]: Generator for coordinates
  """
  angle_tan = tan(radians(angle_deg))
  if angle_deg < 90:
    # Top Right Quadrant
    # Checking x and y points ensures we find the best point in both
    # distance to an integer coordinate and distance from (0,0).
    return [
      x_generator(
        1, upper_bounds, lower_bounds, upper_bounds, angle_tan
        ),
      y_generator(
        1, upper_bounds, lower_bounds, upper_bounds, angle_tan
        )
    ]

  if angle_deg < 180:
    # Top left Quadrant
    # Step -1 ensures better symmetery in coordinate placement.
    # Checking outwards in prioritizes coordinates closer to (0,0).
    return [
      x_generator(
        -1, -upper_bounds, lower_bounds, upper_bounds, angle_tan, step=-1
        ),
      y_generator(
        1, upper_bounds, lower_bounds, upper_bounds, angle_tan
        )
    ]

  if angle_deg < 270:
    # Bottom left Quadrant
    return [
      x_generator(
        -1, -upper_bounds, lower_bounds, upper_bounds, angle_tan, step=-1
        ),
      y_generator(
        -1, -upper_bounds, lower_bounds, upper_bounds, angle_tan, step=-1
        )
    ]

  if angle_deg < 360:
    # Bottom right Quadrant
    return [
      x_generator(
        1, upper_bounds, lower_bounds, upper_bounds, angle_tan
        ),
      y_generator(
        -1, -upper_bounds, lower_bounds, upper_bounds, angle_tan, step=-1
        )
      ]

def custom_sort(
  item: List[Union[int, List[int]]]
  ) -> Tuple[int, int]:
  """
  Return values to sort distance from coordinate, followed by distance from 
  origin.

  Args:
    item (List[Union[int, List[int]]]): Distance from integer coordinate, 
    followed by coordinates.
  Returns:
    List(Tuple[int, int]): Distance from integer coordinate, Distance 
    from [0,0] coordinate. 
  """
  p_key = item[0]
  coordinates = item[1]
  s_key = distance_between_two_points([0, 0], coordinates)
  return (p_key, s_key)

def coordinate_placement(
  count: int,
  offset: Tuple[float] = (0, 0),
  minimum: int = 10,
  maximum: int = 20
  ) -> List[Tuple[int]]:
  """
  Creates a set of coordinates around a centerpoint equally seperated by 
  angle.
  Each point isplaced at their closest integer coordinate within the bounds 
  provided. 

  Args:
    count (int): Amount of desired points
    offset (List[int]): Value to offset the centerpoint
    minimum (int): Minimum radius a point can be at
    maximum (int): Maximum adius a point can be at

  Returns:
    List(Tuple(int)): A list of all points as tuples
  """
  result = []
  epsilon = 1e-10
  lower_bounds = minimum
  upper_bounds = maximum

  for i in range(count):
    points = []
    tolerance_array = []

    angle_deg = (360 / count) * (i + 1)
    # angle_deg = 356.25

    # Axis need edge cases because tan(degrees) will result in divide by
    # zero errors otherwise.
    if angle_deg in [0,90,180,270,360]:
      x = cos(radians(angle_deg))
      y = sin(radians(angle_deg))

      if abs(y) < epsilon:
        if x > 0:
          result.append([lower_bounds, 0])
        else:
          result.append([-lower_bounds, 0])

      elif abs(x) < epsilon:
        if y > 0:
          result.append([0,lower_bounds])
        else:
          result.append([0,-lower_bounds])
      continue

    points = coordinate_generator(lower_bounds, upper_bounds, angle_deg)
    points = list(chain.from_iterable(points))
    for x, y in points:
      tolerance_array.append(distance_to_centerpoint(x, y))

    arr = list(zip(tolerance_array, points))
    arr.sort(key=custom_sort)
    result.append([round(num) for num in arr[0][1]])

  result = [[x + offset[0], y + offset[1]] for x,y in result]
  result = [tuple(arr) for arr in result]

#   if len(result) != len(set(result)):
#     raise Warning("Not all coordinates are unique. Consider changing the \
# minimum and maximum radius.'")
  if len(result) != count:
    raise Warning("Not all coordinates were generated. Consider changing \
the minimum and maximum radius.'")
  return result
