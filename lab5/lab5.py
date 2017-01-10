# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        return id_tree.get_node_classification()
    else:
        id_tree = id_tree.apply_classifier(point)
        return id_tree_classify_point(point,id_tree)


def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    classified = {}
    for i in data:
        choice = classifier.classify(i)
        if choice in classified:
            classified[choice].append(i)
        else:
            classified[choice]=[i]
    return classified

#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    classified = split_on_classifier(data, target_classifier)
    disorder = 0
    for n in classified:
        fraction = float(len(classified[n]))/len(data)
        disorder -= (fraction) * log2(fraction)
    return disorder

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    test_dict = split_on_classifier(data, test_classifier)
    avg_disorder = 0
    for t in test_dict:
        disorder = branch_disorder(test_dict[t],target_classifier)
        avg_disorder += disorder * len(test_dict[t]) / float(len(data))
    return avg_disorder

## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))


#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    min_disorder = INF
    for test in possible_classifiers:
        avg_disorder = average_test_disorder(data, test, target_classifier)
        if avg_disorder < min_disorder:
            best_test = test
            min_disorder = avg_disorder
    if len(split_on_classifier(data, best_test))==1:
        raise NoGoodClassifiersError
    return best_test

## To find the best classifier from 2014 Q2, Part A, uncomment:
#print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))


def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if not id_tree_node:
        id_tree_node = IdentificationTreeNode(target_classifier)

    length = len( split_on_classifier(data, target_classifier).keys() )

    if length == 1:
        classified = target_classifier.classify(data[0])
        id_tree_node.set_node_classification(classified)
        return id_tree_node


    try:
        best_test = find_best_classifier(data, possible_classifiers, target_classifier)

        grouping = split_on_classifier(data, best_test)
        id_tree_node.set_classifier_and_expand(best_test, grouping)

    except NoGoodClassifiersError:
        return id_tree_node

    all_branches = id_tree_node.get_branches().items()

    for (feature,cn) in all_branches:
        small_data = grouping[feature]
        construct_greedy_id_tree(small_data, possible_classifiers, target_classifier, cn)

    return id_tree_node

## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### WARM-UP: DISTANCE METRICS

def dot_product(X, Y):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    size = len(X)
    total = 0
    for i in range(size):
        total += X[i] * Y[i]
        #print X[i], Y[i]
        #print total
    return total

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    answer = 0
    for i in v:
        answer += i**2
    return math.sqrt(answer)

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    answer = 0
    coords_1 = point1.coords
    coords_2 = point2.coords
    if len(coords_1) <= len(coords_2):
        for i in range( min( len(coords_1), len(coords_2) ) ):
            answer += (coords_2[i] - coords_1[i]) **2
    return math.sqrt(answer)


def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    answer = 0
    coords_1 = point1.coords
    coords_2 = point2.coords
    if len(coords_1) <= len(coords_2):
        for i in range( min( len(coords_1), len(coords_2) ) ):
            answer += abs(coords_2[i] - coords_1[i])
    return answer

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    answer = 0
    coords_1 = point1.coords
    coords_2 = point2.coords
    for i in range(min(len(coords_1), len(coords_2))):
        if coords_2[i] != coords_1[i]:
                answer +=1
    return answer

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    coords_1 = point1.coords
    coords_2 = point2.coords
    return 1 - (dot_product(coords_1, coords_2)) / (norm(coords_1)* norm(coords_2))


#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    d = []
    a = []
    for spot in data:
        d.append((spot, distance_metric(spot, point)))
    d.sort(key=lambda x: x[0].coords)
    d.sort(key=lambda x: x[1])
    for spot in d:
        a.append(spot[0])
    return a[:k]


def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    closest = get_k_closest_points(point, data, k, distance_metric)
    classified = []
    p = []
    for x in closest:
        classified.append(x.classification)
    for x in classified:
        p.append((x, classified.count(x)))
    return max(p, key = lambda x: x[1])[0]

## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    correct = 0
    for point in data:
        data_copy = data[:]
        data_copy.remove(point)
        classified = knn_classify_point(point, data_copy, k, distance_metric)
        if classified ==  point.classification:
            correct += 1

    all = len(data)
    answer = correct / float(all)
    return answer


def metrics(data, k, measures, baseline, opt):
        for elem in measures:
            cross = cross_validate(data, k, elem)
            if cross > baseline:
                opt = (k, elem)
                baseline = cross
        return opt, baseline


def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    optimal = (0, None)
    base = 0
    measures = [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]
    for k in range(1,10):
        optimal, base = metrics(data, k, measures, base, optimal)
    return optimal



## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3

#### SURVEY ###################################################

NAME = 'Arturo'
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "5"
WHAT_I_FOUND_INTERESTING = "ID trees are cool"
WHAT_I_FOUND_BORING = "not a fan of k nearest"
SUGGESTIONS = ''
