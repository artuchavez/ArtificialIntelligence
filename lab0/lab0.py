# MIT 6.034 Lab 0: Getting Started
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and past 6.034 staff

from point_api import Point

# This is a multiple choice question. You answer by replacing
# the symbol 'None' with a letter, corresponding to your answer.

# What version of Python do we *recommend* (not "require") for this course?
#   A. Python v2.3
#   B. Python v2.5, Python v2.6, or Python v2.7
#   C. Python v3.0
# Fill in your answer in the next line of code ("A", "B", or "C"):

ANSWER_1 = "B"


#### Warm-up: Exponentiation ###################################################

def cube(x):
    "Given a number x, returns its cube (x^3)"
    return x**3


#### Recursion #################################################################

def fibonacci(n):
    "Given a positive int n, uses recursion to return the nth Fibonacci number."
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def expression_depth(expr):
    """Given an expression expressed as Python lists, uses recursion to return
    the depth of the expression, where depth is defined by the maximum number of
    nested operations."""
    if not isinstance(expr, list):
        return 0
    return max(map(expression_depth, expr)) + 1


#### Built-in data types #######################################################

def compute_string_properties(string):
    """Given a string of lowercase letters, returns a tuple containing the
    following three elements:
        0. The length of the string
        1. A list of all the characters in the string (including duplicates, if
           any), sorted in REVERSE alphabetical order
        2. The number of distinct characters in the string (hint: use a set)
    """
    string_length = len(string)
    list_form = list(string)
    list_form.sort(reverse=True)
    distinct = set(list_form)
    return (string_length, list_form, len(distinct))



def tally_letters(string):
    """Given a string of lowercase letters, returns a dictionary mapping each
    letter to the number of times it occurs in the string."""
    tally_dict = {}
    for letter in string:
        tally_dict[letter] = 0
    for letter in string:
        tally_dict[letter] += 1
    return tally_dict


#### Functions that return functions ###########################################

def create_multiplier_function(m):
    "Given a multiplier m, returns a function that multiplies its input by m."
    def multiply_funct(input):
        return input * m
    return multiply_funct



#### Objects and APIs: Copying and modifing objects ##########################

def get_neighbors(point):
    """Given a 2D point (represented as a Point object), returns a list of the
    four points that neighbor it in the four coordinate directions.  Uses the
    "copy" method to avoid modifying the original point."""

    neighbors = []
    for i in [-1,1]:
            new_copy = point.copy()
            new_copy.setX(new_copy.getX() + i)
            new_copy.setY(new_copy.getY() + 0)
            neighbors.append(new_copy)
    for j in [-1,1]:
            new_copy = point.copy()
            new_copy.setX(new_copy.getX() + 0)
            new_copy.setY(new_copy.getY() + j)
            neighbors.append(new_copy)
    return neighbors


#### Using the "key" argument ##################################################

def sort_points_by_Y(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "sorted"
    with the "key" argument to create and return a list of the points sorted in
    increasing order based on their Y coordinates, without modifying the
    original list."""
    sorting_func = lambda point: point.getY()
    return sorted(list_of_points, key=sorting_func)

def furthest_right_point(list_of_points):
    """Given a list of 2D points (represented as Point objects), uses "max" with
    the "key" argument to return the point that is furthest to the right (that
    is, the point with the largest X coordinate)."""
    sorting_fun = lambda point: point.getX()
    return max(list_of_points, key= sorting_fun)



#### SURVEY ####################################################################

# How much programming experience do you have, in any language?
#     A. No experience (never programmed before this semester)
#     B. Beginner (just started learning to program, e.g. took one programming class)
#     C. Intermediate (have written programs for a couple classes/projects)
#     D. Proficient (have been programming for multiple years, or wrote programs for many classes/projects)
#     E. Expert (could teach a class on programming, either in a specific language or in general)

PROGRAMMING_EXPERIENCE = "C"  #type a letter (A, B, C, D, E) between the quotes


# How much experience do you have with Python?
#     A. No experience (never used Python before this semester)
#     B. Beginner (just started learning, e.g. took 6.0001)
#     C. Intermediate (have used Python in a couple classes/projects)
#     D. Proficient (have used Python for multiple years or in many classes/projects)
#     E. Expert (could teach a class on Python)

PYTHON_EXPERIENCE = "C"


# Finally, the following questions will appear at the end of every lab.
# The first three are required in order to receive full credit for your lab.

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 2
SUGGESTIONS = None #optional
