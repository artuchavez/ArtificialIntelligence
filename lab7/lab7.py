# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff
import math
from svm_data import *

# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    output = 0
    for i in range(len(u)):
        output += (u[i]*v[i])
    return output

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    answer = 0
    for i in v:
        answer += i**2
    final_answer = math.sqrt(answer)
    return final_answer

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    w = svm.w
    b = svm.b
    x = point.coords
    return dot_product(w, x) + b

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    label = positiveness(svm, point)
    if label > 0:
        return 1
    elif label < 0:
        return -1
    else:
        return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2/norm(svm.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    violations = set()
    for point in svm.training_points:
        if point in svm.support_vectors:
            if point.classification != positiveness(svm, point):
                violations.add(point)

        if positiveness(svm, point) < 1 and positiveness(svm, point) > -1:
            violations.add(point)

    return violations

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    violations = set()
    for point in svm.training_points:
        if point not in svm.support_vectors:
            if point.alpha != 0:
                violations.add(point)
        else:
            if point.alpha <= 0:
                violations.add(point)
    return violations

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    vector = []
    boundary = 0

    for point in svm.training_points:
        vector.append(scalar_mult(point.classification * point.alpha, point.coords))
        boundary += point.classification * point.alpha

    sum = vector.pop(0)

    for point in vector:
        sum = vector_add(sum, point)

    if boundary == 0:
        if sum == svm.w:
            return True

    return False

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    violations = set()
    for point in svm.training_points:
        if point.classification != classify(svm, point):
            violations.add(point)

    return violations

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""
    supports = []
    for point in svm.training_points:
        if point.alpha > 0:
            supports.append(point)
    svm.support_vectors = supports

    w = (0,0)
    for v in svm.training_points:
        w = vector_add(w, scalar_mult(v.alpha * v.classification, v.coords))
    svm.w = w

    min = 100000
    max = -100000
    for v in svm.support_vectors:
        b = -1 * dot_product(svm.w, v) + v.classification
        if v.classification == 1:
            if b > max:
                max = b
        if v.classification == -1:
            if b< min:
                min = b

    svm.b = (min + max)/2.0

    return svm

# Multiple choice
ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = 'AD'
ANSWER_6 = 'ABD'
ANSWER_7 = 'ABD'
ANSWER_8 = []
ANSWER_9 = 'ABD'
ANSWER_10 = 'ABD'

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "4"
WHAT_I_FOUND_INTERESTING = "the visualization"
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
