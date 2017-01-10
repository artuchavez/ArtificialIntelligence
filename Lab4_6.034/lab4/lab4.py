# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem
import itertools

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    domain_dict = csp.domains
    for key in domain_dict.keys():
        if len(domain_dict[key]) == 0:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    for a_name, a_value in csp.assigned_values.iteritems():
        for b_name, b_value in csp.assigned_values.iteritems():
            for constraint in csp.constraints_between(a_name, b_name):
                if not constraint.check(a_value, b_value):
                    return False

    return True

def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    agenda = [problem]
    extensions = 0

    while len(agenda) > 0:
        csp = agenda.pop(0) # get first element from list
        extensions += 1
        if has_empty_domains(csp):
            return (None, extensions)
        elif check_all_constraints(csp):
            if not(csp.unassigned_vars): # all variables assigned!
                return (csp.assigned_values, extensions)
            else:
                var = csp.pop_next_unassigned_var()
                children = []
                for val in csp.get_domain(var):
                    csp_new = csp.copy()
                    csp_new.set_assigned_value(var, val)
                    children.append(csp_new)
                agenda = children + agenda

    return (None, extensions)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    changed = []
    for other_var in csp.unassigned_vars:
        copy_domain = csp.get_domain(other_var)[:]
        for other_val in copy_domain :
            if not any(check_assignments(csp, (var, val), (other_var, other_val)) for val in csp.get_domain(var)):
                csp.eliminate(other_var, other_val)
                if not csp.get_domain(other_var):
                    return None
                if other_var not in changed:
                    changed.append(other_var)
    return sorted(changed)

def check_assignments(csp, var1, var2) :
    """Check if all constraints between var1 and var2 are satisfied for the
    given assignment values"""
    return all(constraint.check(var1[1], var2[1]) for constraint in csp.constraints_between(var1[0], var2[0]))

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    used = []
    if queue == None:
        queue = list(csp.variables)
    while len(queue)>0:
        var = queue.pop(0)
        used.append(var)
        new = eliminate_from_neighbors(csp, var)
        if new == None:
            return None
        for n in new:
            if n not in queue:
                queue.append(n)
    return used


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = solve_constraint_dfs(get_pokemon_problem())[1]

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?

domain_pokemon = get_pokemon_problem()
domain_reduction(domain_pokemon)
ANSWER_2 = solve_constraint_dfs(domain_pokemon)[1]

#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""

    agenda = [problem]
    extensions = 0

    while len(agenda) > 0:
        csp = agenda.pop(0)
        extensions += 1
        if has_empty_domains(csp):
            continue
        elif check_all_constraints(csp):
            if not csp.unassigned_vars:
                return (csp.assigned_values, extensions)
            else:
                var = csp.pop_next_unassigned_var()
                children = []
                for val in csp.get_domain(var):
                    csp_new = csp.copy()
                    csp_new.set_assigned_value(var, val)
                    domain_reduction(csp_new, [var])
                    children.append(csp_new)
                agenda = children + agenda

    return (None, extensions)


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)

ANSWER_3 = solve_constraint_propagate_reduced_domains(get_pokemon_problem())[1]


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    if queue is None:
        queue = list(csp.variables)

    used = []

    while queue:
        var = queue.pop(0)
        used.append(var)
        new_queue = eliminate_from_neighbors(csp, var)

        if new_queue is None:
            return None

        queue.extend((n for n in new_queue if n not in queue and (len(csp.get_domain(n)) == 1)))

    return used

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    agenda = [problem]
    evals = 0

    while len(agenda) > 0:
        csp = agenda.pop(0)
        evals += 1
        if has_empty_domains(csp):
            continue
        elif check_all_constraints(csp):
            if len(csp.unassigned_vars) == 0:
                return (csp.assigned_values, evals)
            else:
                var = csp.pop_next_unassigned_var()
                children = []
                for val in csp.get_domain(var):
                    csp_new = csp.copy()
                    csp_new.set_assigned_value(var, val)
                    domain_reduction_singleton_domains(csp_new, [var])
                    children.append(csp_new)
                agenda = children + agenda

    return (None, evals)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)

ANSWER_4 = solve_constraint_propagate_singleton_domains(get_pokemon_problem())[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    if queue is None:
        queue = csp.variables[:]

    dequeued = []

    while queue:
        var = queue.pop(0)
        dequeued.append(var)
        new_queue = eliminate_from_neighbors(csp, var)

        if new_queue is None:
            return None

        queue.extend((v for v in new_queue if v not in queue and enqueue_condition_fn(csp, v)))
    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var)) == 1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False

#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    agenda = [problem]
    evals = 0

    while len(agenda) > 0:
        csp = agenda.pop(0) # get first element from list
        evals += 1
        if has_empty_domains(csp):
            continue # backtrack
        elif check_all_constraints(csp):
            if not csp.unassigned_vars: # all variables assigned!
                return (csp.assigned_values, evals)
            else:
                var = csp.pop_next_unassigned_var()
                children = []
                for val in csp.get_domain(var):
                    csp_new = csp.copy()
                    csp_new.set_assigned_value(var, val)
                    if enqueue_condition is not None:
                        propagate(enqueue_condition, csp_new, [var])
                    children.append(csp_new)
                agenda = children + agenda
    return (None, evals)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if (m - n) in [-1,1]:
        return True
    return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not constraint_adjacent(m, n)

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    return [Constraint(a, b, constraint_different) for (a, b) in itertools.combinations(variables, 2)]



#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Arturo Chavez-Gehrig"
COLLABORATORS = "Luana Lopes Lara"
HOW_MANY_HOURS_THIS_LAB_TOOK = "8"
WHAT_I_FOUND_INTERESTING = "Cool examples"
WHAT_I_FOUND_BORING = "Unclear API, sometimes felt unintuitive"
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
