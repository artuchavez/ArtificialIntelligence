# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
import math
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    N = len(training_points)
    weight_dict = dict()
    for i in training_points:
        weight_dict[i] = make_fraction(1,N)
    return weight_dict

def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    error_dict = dict()
    for c in classifier_to_misclassified.keys():
        total = 0
        for p in classifier_to_misclassified[c]:
            total += point_to_weight[p]
        error_dict[c] = total
    return error_dict

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    items = classifier_to_error_rate.items()
    if use_smallest_error:
        A = sorted(items, key=lambda name: name[0])
        A = sorted(A, key=lambda each: each[1])
        if A[0][1] == make_fraction(1,2):
            raise NoGoodClassifiersError()
        return A[0][0]


    else:

        B = sorted(items, key=lambda name: name[0])
        B = sorted(B, key=lambda classifier: abs(make_fraction(1,2) - make_fraction(classifier[1])), reverse=True)
        if classifier_to_error_rate[B[0][0]] == make_fraction(1,2):
            print 'hi'
            raise NoGoodClassifiersError()

        return B[0][0]

def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 1.0:
        return -INF
    elif error_rate == 0.0:
        return INF
    else:
        return make_fraction(1,2) * ln(make_fraction(1-error_rate, error_rate))

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    total_vote = 0
    vote_dict = dict()
    for v in training_points:
        vote_dict[v] = 0
    for h in H:
        score = h[1]
        total_vote += score
        for v in classifier_to_misclassified[h[0]]:
            vote_dict[v] += score
    answer = set()
    for point in training_points:
        if vote_dict[point] >= .5 * total_vote:
            answer.add(point)
    return answer

def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    wrong = get_overall_misclassifications(H,training_points,classifier_to_misclassified)
    return len(wrong) <= mistake_tolerance

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    answer = dict()
    misclassified = set(misclassified_points)
    for p in point_to_weight:
        if p in misclassified:
            answer[p] = make_fraction(1,2) * make_fraction(1, error_rate) * point_to_weight[p]
        else:
            answer[p] = make_fraction(1,2) * make_fraction(1, 1 - error_rate) * point_to_weight[p]
    return answer

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    weights = initialize_weights(training_points)
    H = []

    iteration = 1
    while iteration <= max_rounds:
        if is_good_enough(H,training_points, classifier_to_misclassified, mistake_tolerance):
            return H
        iteration += 1

        error_rates = calculate_error_rates(weights, classifier_to_misclassified)
        #print error_rates
        try:
            h = pick_best_classifier(error_rates, use_smallest_error)
            power = calculate_voting_power(error_rates[h])
            H.append((h, power))
            weights = update_weights(weights,classifier_to_misclassified[h], error_rates[h])
        except NoGoodClassifiersError:
            #print 'hello'
            break

    return H

#### SURVEY ####################################################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'sorted python built in function is very nice'
WHAT_I_FOUND_BORING = 'nothing'
SUGGESTIONS = ''
