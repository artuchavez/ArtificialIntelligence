# MIT 6.034 Lab 2: Search
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    if len(path) < 2:
        return 0
    total_length = 0
    for i in range(len(path)-1):
        edge = graph.get_edge(path[i], path[i + 1])
        weight = edge.length
        total_length += weight
    return total_length

def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    visited = {}
    for node in path:
        if node not in visited:
            visited[node] = 0
        else:
            return True
    return False


def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    neighbors = graph.get_neighbors(path[-1])
    extensions = []
    for node in neighbors:
        new_path = path[:]
        new_path.append(node)
        if has_loops(new_path):
            continue
        else:
            extensions.append(new_path)
    extensions.sort()
    return extensions



def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a lower heuristic to be "better" because it represents a shorter
    potential path to the goal. Break ties lexicographically by node name."""
    with_heuristic = []
    for node in nodes:
        estimate = graph.get_heuristic_value(node,goalNode)
        with_heuristic.append((estimate,node))
    with_heuristic.sort(key= grab_second_elt)
    with_heuristic.sort(key= grab_first_elt)
    answer = []
    for tup in with_heuristic:
        answer.append(tup[1])
    return answer

def grab_second_elt(thing):
    return thing[1]
def grab_first_elt(thing):
    return thing[0]

# You can ignore the following line.  It allows generic_search (PART 2) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Generic Search ####################################################

# Note: If you would prefer to get some practice with implementing search
# algorithms before working on Generic Search, you are welcome to do PART 3
# before PART 2.

# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:


def break_ties(paths):
    return sorted(paths)


# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]


def hill_climb_sort(graph, goalNode, paths):
    new_paths = break_ties(paths)
    with_heur = []
    for path in new_paths:
        last_node = path[-1]
        estimate = graph.get_heuristic_value(last_node,goalNode)
        with_heur.append((path,estimate))

    with_heur.sort(key= grab_second_elt)
    answer = []
    for tup in with_heur:
        answer.append(tup[0])
    return answer

def branch_sort(graph, goal, paths):
    new_paths = break_ties(paths)
    total_lengths = []
    for path in new_paths:
        total = 0
        for i in range(len(path)-1):
            edge = graph.get_edge(path[i],path[i+1])
            total += edge.length
        total_lengths.append((path,total))
    total_lengths.sort(key= grab_second_elt)
    answer = []
    for tup in total_lengths:
        answer.append(tup[0])
    return answer

def branch_sort_heur(graph, goal, paths):
    new_paths = break_ties(paths)
    total_lengths = []
    for path in new_paths:
        last_node = path[-1]
        estimate = graph.get_heuristic_value(last_node,goal)
        total = estimate
        for i in range(len(path)-1):
            edge = graph.get_edge(path[i],path[i+1])
            total += edge.length
        total_lengths.append((path,total))
    total_lengths.sort(key= grab_second_elt)
    answer = []
    for tup in total_lengths:
        answer.append(tup[0])
    return answer

generic_hill_climbing = [hill_climb_sort, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, True, hill_climb_sort, False]

generic_branch_and_bound = [do_nothing_fn, True, branch_sort, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, True, branch_sort_heur, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, False, branch_sort, True]

generic_a_star = [do_nothing_fn, False, branch_sort_heur, True]

# Here is an example of how to call generic_search (uncomment to run):
#my_dfs_fn = generic_search(*generic_dfs)
#my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
#print my_dfs_path

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]

# Uncomment this to test your generic_beam search:
#print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 3: Search Algorithms #################################################

# Note: It's possible to implement the following algorithms by calling
# generic_search with the arguments you defined in PART 2.  But you're also
# welcome to code them without using generic_search if you would prefer to
# implement the algorithms by yourself.

def dfs(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_dfs)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path

def bfs(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_bfs)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path

def hill_climbing(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_hill_climbing)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path


def best_first(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_best_first)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path

def beam(graph, startNode, goalNode, beam_width):
    agenda = [([startNode], 0)]
    level_count = {0: 1}
    level_to_paths = [[startNode]]

    while len(agenda) > 0:
        current_path_tuple = agenda.pop(0)
        currentPath = current_path_tuple[0]
        current_level = current_path_tuple[1]

        terminal_node = currentPath[len(currentPath)-1]
        if terminal_node == goalNode: return currentPath

        neighbors = graph.get_neighbors(terminal_node)
        new_paths = []
        for n in neighbors:
            if n not in currentPath:
                new_path = currentPath[:]
                new_path.append(n)
                new_paths.append(new_path)

                if len(level_to_paths)<=current_level+1:
                    newLevelPathList = [new_path]
                    level_to_paths.append(newLevelPathList)
                    level_count[current_level+1] = 1
                else:
                    oldLevelPathList = level_to_paths[current_level+1]
                    newLevelPathList = oldLevelPathList[:]
                    newLevelPathList.append(new_path)

                    level_to_paths[current_level+1] = newLevelPathList
                    level_count[current_level+1] += 1

        for level in level_count.keys():
            if level_count[level] > beam_width:
                allPaths = level_to_paths[level]
                allPaths = sorted(allPaths, key=lambda path:
                                  graph.get_heuristic_value(path[len(path)-1], goalNode))
                newPathList = allPaths[0:beam_width]
                level_to_paths[level] = newPathList
                level_count[level] = beam_width

                purgedPaths = allPaths[beam_width:]
                for pp in purgedPaths:
                    if pp in new_paths: new_paths.remove(pp)
                    if (pp, level) in agenda: agenda.remove((pp, level))
        for np in new_paths:
            agenda.append((np, current_level+1))

    return None

def branch_and_bound(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_branch_and_bound)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path


def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_branch_and_bound_with_heuristic)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path


def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_branch_and_bound_with_extended_set)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path


def a_star(graph, startNode, goalNode):
    my_dfs_fn = generic_search(*generic_a_star)
    my_dfs_path = my_dfs_fn(graph, startNode, goalNode)
    return my_dfs_path


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    for node in graph.nodes:
        heuristic = graph.get_heuristic_value(node, goalNode)
        shortestPath = a_star(graph, node, goalNode)
        shortestDist = path_length(graph, shortestPath)

        if heuristic > shortestDist: return False

    return True


def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    for e in graph.edges:
        diff = abs(graph.get_heuristic_value(e.startNode, goalNode) - graph.get_heuristic_value(e.endNode, goalNode))
        if e.length < diff: return False
    return True


### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 6
WHAT_I_FOUND_INTERESTING = 'really building an understanding of the individual components of a search alg'
WHAT_I_FOUND_BORING = 'there is a lot of repetition in this lab'
SUGGESTIONS = ''


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]