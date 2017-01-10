# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
import math

INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    return int(x >= threshold)

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1.0 / (1 + math.e ** (-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0,x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -.5 * (desired_output - actual_output)**2

# Forward propagation
def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    new_net = net.topological_sort()
    values = input_values
    dictionary = {}
    for neuron in new_net:
        sum = 0
        for node in net.get_incoming_neighbors(neuron):
            sum += node_value(node, values, dictionary) * net.get_wires(node, neuron)[0].weight
        output = threshold_fn(sum)
        dictionary[neuron] = output
        values[neuron] = output

    return (dictionary[new_net[-1]], dictionary)

# Backward propagation warm-up
def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    back_step = step_size * -1
    changes = [0, back_step, step_size]
    maxim = -INF
    point = []
    a_init = inputs[0]
    b_init = inputs[1]
    c_init = inputs[2]
    for elt in changes:
        a = a_init + elt
        for elem in changes:
            b = b_init + elem
            for ele in changes:
                c = c_init + ele
                out = func(a,b,c)
                if out > maxim:
                    maxim = out
                    point = [a,b,c]
    return (maxim, point)


def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""

    finalSet = set()
    agenda = [wire.endNode]
    while agenda:
        outgoing = net.get_outgoing_neighbors(agenda[0])
        neuron = agenda.pop(0)
        finalSet.add(neuron)
        if net.is_output_neuron(neuron):
            finalSet.add(wire)
            finalSet.add(wire.startNode)
        else:
            for n in outgoing:
                agenda.append(n)
                newWire = net.get_wires(neuron, n)[0]
                finalSet.add(newWire)
                finalSet.add(n)
    return finalSet

"""
    important = set()
    queue = [wire.startNode]
    while queue:
        node = queue.pop()
        important.add(node)
        if net.is_output_neuron(node):
            important.add(wire)
            important.add(wire.startNode)
        else:
            for n in net.get_outgoing_neighbors(node):
                #if n not in important:
                    queue.append(n)
                    newWire = net.get_wires(node, n)[0]
                    important.add(newWire)
                    important.add(n)
    return important
"""
# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """

    deltas = {}
    intermediate_values = neuron_outputs
    for neuron in reversed(net.topological_sort()):
        current = intermediate_values[neuron]
        if net.is_output_neuron(neuron):
            deltas[neuron] = current * (1 - current) * (desired_output - current)
        else:
            deltas[neuron] = current * (1 - current) * sum(w.get_weight() * deltas[w.endNode] for w in net.get_wires(neuron))
    return deltas

def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""

    delta_B = calculate_deltas(net, desired_output, neuron_outputs)

    for wire in net.get_wires():
        if wire.startNode in set(net.inputs) and wire.startNode in input_values:
            old = wire.get_weight()
            new_weight = old + r * input_values[wire.startNode] * delta_B[wire.endNode]
            wire.set_weight(new_weight)
        else:
            old = wire.get_weight()
            if wire.startNode not in neuron_outputs:
                new_weight = old + r * wire.startNode * delta_B[wire.endNode]
            else:
                new_weight = old + r * neuron_outputs[wire.startNode] * delta_B[wire.endNode]
            wire.set_weight(new_weight)
    return net

def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    (final, outputs) = forward_prop(net, input_values, sigmoid)
    iteration = 0
    while accuracy(desired_output, final) <= minimum_accuracy:
        update_weights(net, input_values, desired_output, outputs, r)
        (final, outputs) = forward_prop(net, input_values, sigmoid)
        iteration += 1

    return (net, iteration)


# Training a neural net

ANSWER_1 = 17
ANSWER_2 = 34
ANSWER_3 = 8
ANSWER_4 = 145
ANSWER_5 = 65

ANSWER_6 = 1
ANSWER_7 = 'checkerboard'
ANSWER_8 = ['small','medium', 'large']
ANSWER_9 = 'b'

ANSWER_10 = 'd'
ANSWER_11 = "AC"
ANSWER_12 = "AE"


#### SURVEY ####################################################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = '10'
WHAT_I_FOUND_INTERESTING = 'neural nets are cooool!'
WHAT_I_FOUND_BORING = 'nothing'
SUGGESTIONS = ''
