# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)'), THEN('(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:
# if x is the parent of y, then y is the child of x
# if x is a parent of y AND y is a parent of z, then x is the grandparent of z AND z is the grandchild of x
# if x is the parent of y and x is the parent of z, Then x is the sibling of y AND y is the sibling of x
# if x is the child of y AND y is the sibling of z AND a is the child of z, then x and a are cousins and a and x are cousins
#

#( IF( AND( '(?x) has feathers',  # rule 1
#          '(?x) has a beak' ),
#    THEN( '(?x) is a bird' )),)
#  IF( AND( '(?y) is a bird',     # rule 2
#           '(?y) cannot fly',
#           '(?y) can swim' ),
#      THEN( '(?y) is a penguin' ) ) )



self_rule = IF('person (?x)', THEN( 'self (?x) (?x)') )
child_rule =  IF('parent (?x) (?y)', THEN( 'child (?y) (?x)'))
grandparent_rule = IF( AND( 'parent (?x) (?y)', 'parent (?y) (?z)'), THEN( 'grandparent (?x) (?z)', 'grandchild (?z) (?x)' ))
sibling_rule = IF( AND('parent (?x) (?y)', 'parent (?x) (?z)', NOT('self (?y) (?z)')), THEN( 'sibling (?y) (?z)','sibling (?z) (?y)'))
cousin_rule = IF( AND('child (?x) (?y)', 'sibling (?y) (?z)', 'child (?a) (?z)'), THEN( 'cousin (?x) (?a)', 'cousin (?a) (?x)'))


# Add your rules to this list:
family_rules = [self_rule, child_rule, grandparent_rule, sibling_rule, cousin_rule]

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins
#print len(black_family_cousins)

#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """
    if len(rules)==0:
        return hypothesis

    tree = OR()

    for rule in rules:
        consequent = rule.consequent()
        m = match(consequent[0], hypothesis)
        if m != None and len(m) >= 0:
            antecedent = rule.antecedent()

            if isinstance(antecedent, list):
                logic = AND()
                if isinstance(antecedent, OR):
                    logic= OR()
                for a in antecedent:
                    new_tree = backchain_to_goal_tree(rules, populate(a, m))
                    logic.append(new_tree)
                tree.append(logic)
            else:
                new_tree = backchain_to_goal_tree(rules, populate(antecedent, m))
                tree.append(AND(new_tree))

        else:
            tree.append(hypothesis) #LEAF

    return simplify(tree)

# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = '6'
WHAT_I_FOUND_INTERESTING = 'rule based systems are powerful, I liked the familiar relationships one'
WHAT_I_FOUND_BORING = 'I think the backchaining question was pretty confusing'
SUGGESTIONS = 'more review of backchaining and this type of programming in recitation'


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
