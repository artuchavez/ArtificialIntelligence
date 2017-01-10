# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *

#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors = set()
    parents = net.get_parents(var)
    queue = list(parents)
    while queue:
        parent = queue.pop()
        ancestors.add(parent)
        queue.extend(list(net.get_parents(parent)))
    return ancestors


def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = set()
    children = net.get_children(var)
    queue = list(children)
    while queue:
        child = queue.pop()
        descendants.add(child)
        queue.extend(list(net.get_children(child)))
    return descendants

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    desc = get_descendants(net,var)
    non_desc = set()
    for each in net.get_variables():
        if each not in desc and each != var:
            non_desc.add(each)
    return non_desc

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""
    non_desc = get_nondescendants(net,var)
    desc = get_descendants(net,var)
    parents = net.get_parents(var)
    if parents.issubset(givens):
        for elt in desc:
            if elt in givens:
                return givens
        if not desc.issubset(givens):
            answer = {}
            for p in parents:
                answer[p] = givens[p]
            return answer
    return givens


#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    try:
        if givens is not None:
            simplified = simplify_givens(net, hypothesis.keys()[0], givens)
            return net.get_probability(hypothesis, simplified, True)
        else:
            return net.get_probability(hypothesis, givens, True)
    except ValueError:
        raise LookupError()
    raise LookupError()

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    top_sort = net.topological_sort()

    answer = 1

    for each in top_sort:
        if each in hypothesis:
            givens = {}
            new_hyp = {}
            new_hyp[each] = hypothesis[each]
            # del hypothesis[each]
            for elt in net.get_parents(new_hyp.keys()[0]):
                givens[elt] = hypothesis[elt]
            answer = answer * probability_lookup(net, new_hyp, givens)

    return answer

def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    top_sort = net.topological_sort()
    combos = net.combinations(top_sort, hypothesis)
    sum = 0
    for each in combos:
        sum += probability_joint(net, each)
    return sum


def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    try:
        if givens is not None:
            for each in hypothesis.keys():
                if each in givens:
                    if givens[each] != hypothesis[each]:
                        return 0.0
                    else:
                        return 1.0
        return probability_lookup(net,hypothesis,givens)
    except LookupError:
        if givens is not None:
            d3 = dict(hypothesis, **givens)
        else:
            d3 = hypothesis
        top = probability_marginal(net, d3)
        bottom = probability_marginal(net,givens)
        return top/bottom



def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    variables = net.get_variables()
    answer = 0
    for var in variables:
        domain_size = len(net.get_domain(var)) - 1
        prod = 1
        for p in net.get_parents(var):
            prod = prod * len(net.get_domain(p))
        answer += domain_size * prod
    return answer


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    for elem in net.get_domain(var1):
        for elt in net.get_domain(var2):
            p_1 = probability(net, {var1 : elem}, givens)
            p_2 = probability(net, {var2 : elt}, givens)
            p_3 = probability(net, {var1 : elem, var2 : elt}, givens)
            if approx_equal(p_1 * p_2, p_3):
                continue
            else:
                return False
    return True


def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""

    variables = set()
    a = [var1, var2]
    a.extend(list(get_ancestors(net,var1)))
    a.extend(list(get_ancestors(net,var2)))
    variables.update(set(a))
    if givens is not None:
        for elt in givens:
            variables.add(elt)
            variables.update(get_ancestors(net, elt))
    ancestral_graph = net.subnet(list(variables))
    copy_net = ancestral_graph.subnet(ancestral_graph.get_variables())
    for each in copy_net.get_variables():
        parents = copy_net.get_parents(each)
        for mom in parents:
            for dad in parents:
                if mom != dad:
                    ancestral_graph.link(mom,dad)

    bidirectional_net = ancestral_graph.make_bidirectional()
    if givens is not None:
        for each in givens.keys():
            bidirectional_net.remove_variable(each)
    return bidirectional_net.find_path(var1,var2) == None


#### SURVEY ####################################################################

NAME = 'Arturo'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
