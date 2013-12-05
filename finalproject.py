import os
import sys
from math import sin
import random
import copy

#Constants
NUM_TREES = 100
TOP_PERCENT = 0.2
BOTTOM_PERCENT = 0.8
TOP_PERCENT_PROPORTION = .8
BOTTOM_PERCENT_PROPORTION = .2
INVALID_RETURN = 9999999999
WINNING_ERROR_BOUND = 500
MAX_GENERATIONS = 10

NUM_PERMITTED_NESTED_EXPONENTS = 2

operators = ['+', '-', '*', '/', 'sin', '^']
file_data = []
tree_roots = []
equations = []


class EquationNode:
    eq = ''
    left = None
    right = None
    data = None
    def __init__(self, data=None):
        self.data = data

class TreeData:
    node = None
    equation = ''
    error = 0

    def __init__(self, node, equation, error):
        self.node = node
        self.equation = equation
        self.error = error


def parseTree(current_node):
    eq = ''
    if current_node.left is not None and current_node.data != 'sin':
        eq += '('
        eq += parseTree(current_node.left)
    eq += str(current_node.data)
    if current_node.data == 'sin' and current_node.left is not None:
        eq += '('
        eq += parseTree(current_node.left)
    if current_node.left is not None and current_node.right is None:
        eq += ')'
    elif current_node.right is not None and current_node.left is None:
        eq += '('
    if current_node.right is not None:
        eq += parseTree(current_node.right)
        eq += ')'
    return eq.replace('^', '**')

#This will need to be called recursively
def assign_node_values(current_node, current_depth, need_x, max_depth):
            left = 0
            right = 0
            double_operators = ['+', '-', '*', '/', '^']
            single_operators = ['sin']
            possible_values = ['+', '-', '*', '/', 'sin', '^', 'num', 'x', 'num', 'num']

            #check to see if we have been called on a node that is not an operator
            if current_node.data not in operators:
                return
            #check to see if we are already at max depth
            #if we are max depth and still need x, then override the current_node.data with x
            #otherwise, exit the recursion
            if current_depth == max_depth:
                if need_x is True:
                    current_node.data = 'x'
                    return
                else:
                    return
            #if the current depth+1 is the max depth, then the children must be set to x or a number, not an op
            if (current_depth+1) == max_depth:
                possible_values = ['num', 'x']
            #if the current operator is a single operator, set one of the children to None
            if current_node.data in single_operators:
                #will the single leg be on the left or right?
                leg = random.choice(['left', 'right'])
                if leg == 'left':
                    right = None
                elif leg == 'right':
                    left = None
            #we are not second from the bottom nor the bottom, and we are clear to choose any value
            if left is not None:
                left = random.choice(possible_values)
                if left == 'num':
                    left = random.randrange(0, 100)
                elif left == 'x':
                    need_x = False
                current_node.left = EquationNode(left)
                assign_node_values(current_node.left,current_depth+1,need_x,max_depth)
            if right is not None:
                right = random.choice(possible_values)
                if right == 'num':
                    right = random.randrange(0,100)
                elif left == 'x':
                    need_x = False
                current_node.right = EquationNode(right)
                assign_node_values(current_node.right,current_depth+1,need_x,max_depth)

#we need to perform a check for nested exponentials because they either take forever to evaluate or they
#cause some seriously long computation times. For now, get right of any case where there are three ** occurrences
#in the equation
def nested_exponential_check(eq):
    count = eq.count('**')
    if count >= NUM_PERMITTED_NESTED_EXPONENTS:
        return True
    else:
        return False

def read_file(filename):
    f = open(filename, 'r')
    line = f.readline()
    if line != '':
        file_data.append(line.replace('\n',''))
    while line != '':
        line = f.readline()
        if line != '':
            file_data.append(line.replace('\n',''))

def calc_rms_error(equation, data_array):
    squares = []
    for entry in data_array:
        l = entry.split(',')
        x = int(l[0])
        y = int(l[1])
        #need to keep from having imaginary elements in there... that causes an error
        #so immediately return the value of the thing has sin(sin(x)) in it
        if 'sin(sin' in equation:
            return INVALID_RETURN
        #another check for an edge case: nested exponents
        if nested_exponential_check(equation) is True:
            return INVALID_RETURN
        try:
            ans = eval(equation.replace('x', str(x)))
        except ZeroDivisionError:
            return INVALID_RETURN
        except OverflowError:
            return INVALID_RETURN
        #we need this check to get rid of things with an imaginary component
        except TypeError:
            return INVALID_RETURN
        #we need to keep this from having a complex component as well, because we can't sort by it
        if isinstance(ans, complex):
            return INVALID_RETURN
        try:
            squares.append((y-ans)**2)
        except OverflowError:
            return INVALID_RETURN
    ssum = 0
    try:
        for square in squares:
            ssum += square
        ssum = ssum / len(squares)
    except OverflowError:
            return INVALID_RETURN
    return ssum ** 0.5


def create_random_trees():
    for x in range(0, NUM_TREES):
        node = EquationNode(random.choice(operators))
        assign_node_values(node, 0, True, 4)
        eq = parseTree(node)
        #print(eq)
        tree_roots.append(TreeData(node, eq, calc_rms_error(eq, file_data)))


def print_equations(tree):
    for node in tree:
        print(node.equation)


#this function will go through and to see if we are within WINNING_ERROR_BOUND of the correct answer
def check_for_winner():
    for tree in tree_roots:
        if tree.error <= WINNING_ERROR_BOUND:
            print('We have a winner! The winning equation is: ' + str(tree.equation))
            return True
    return False


def count_operator_nodes(tree, count):
    if tree.data in operators:
        count = count + 1
    if tree.left is not None:
        count = count_operator_nodes(tree.left, count)
    if tree.right is not None:
        count = count_operator_nodes(tree.right, count)
    return count


#This will return a copy of the root node that points to a full copy of the provided tree
def copy_tree(root):
    new_root = EquationNode(root.data)
    if root.left is not None:
        new_root.left = copy_tree(root.left)
    if root.right is not None:
        new_root.right = copy_tree(root.right)
    return new_root


def get_node_at_operator_location_interior(tree, l):
    if tree.data in operators:
        l.append(tree)
    if tree.left is not None:
        get_node_at_operator_location_interior(tree.left, l)
    if tree.right is not None:
        get_node_at_operator_location_interior(tree.right, l)

#get a node that appears at a certain level. The location will be based off of the count_operator_nodes() return value
#this function will return the root of the subtree
def get_node_at_operator_location(root, node_location):
    l = []
    get_node_at_operator_location_interior(root, l)
    return l[node_location-1]


#this function will replace the node at a certain subtree level with the provided subtree_root
#The location value will be based off of the count_operator_nodes() return value
def replace_node_at_operator_location(root, location, current_location, subtree_root):
    if root.data in operators:
        current_location = current_location + 1
    if current_location + 1 == location and root.left is not None:
        print("Replacing")
        print(parseTree(root))
        root.left = subtree_root
        print(parseTree(root.left))
    elif current_location + 1 == location and root.right is not None:
        print("Replacing")
        print(parseTree(root))
        root.right = subtree_root
        print(parseTree(root.right))
    elif root.left is not None:
        current_location = replace_node_at_operator_location(root.left, location, current_location, subtree_root)
    elif root.right is not None:
        current_location = replace_node_at_operator_location(root.right, location, current_location, subtree_root)
    return current_location


def produce_next_generation():
    #we want to take 80% of our stuff from the top 20%
    top_percentage_count = int(TOP_PERCENT * len(tree_roots))
    bottom_percentage_count = int(BOTTOM_PERCENT * len(tree_roots))

    #sort the tree
    sorted_trees = sorted(tree_roots, key=lambda node: node.error)

    #store the newly-created trees in here temporarily -- they will replace tree_roots when this function returns
    descendants = []

    #perform a certain percentage of the combinations only from the top percentage of the parents
    for x in range(0, top_percentage_count):
        tree1_index = 0
        tree2_index = 0
        #get non-identical indexes
        while tree1_index == tree2_index:
            tree1_index = random.randrange(0, top_percentage_count)
            tree2_index = random.randrange(0, top_percentage_count)
        #get random trees to combine from the sorted_trees list
        tree1 = sorted_trees[tree1_index]
        tree2 = sorted_trees[tree2_index]

        #now randomly recombine nodes from tree1 onto tree2
        #traverse the trees to figure out how many non-number or x nodes they have
        op_count_1 = count_operator_nodes(tree1.node, 0)
        op_count_2 = count_operator_nodes(tree2.node, 0)

        #we want to randomly pick a subtree to replace and a subtree to replace it
        if op_count_1+1 <= 2 or op_count_2+1 <= 2:
            continue
        node_1 = random.randrange(2, op_count_1+1)
        node_2 = random.randrange(2, op_count_2+1)

        #randomly decide whether to pick from tree1 or tree2
        donator_choice = random.randrange(0, 2)
        #if donator_choice == 0:
        #pick from tree 1 and place onto tree 2, store in descendants
        donated_node = get_node_at_operator_location(tree1.node, node_1)
        new_donated_node = copy_tree(donated_node)
        print("Adding subtree " + parseTree(donated_node) + " at location " + str(node_2))
        #we are going to want to copy this tree before we stick stuff into it, in case we want to save the parent
        new_root = copy_tree(tree2.node)
        print("Equation before: " + str(parseTree(new_root)))
        replace_node_at_operator_location(new_root, node_2, 0, new_donated_node)
        print("Equation after: " + str(parseTree(new_root)))
        print()
        #elif donator_choice == 1:
        #    #pick from tree 2 and place onto tree 1, store in descendants
        #    donated_node = get_node_at_operator_location(tree2.node, node_2)
        #    new_donated_node = copy_tree(donated_node)
        #    print("Adding subtree " + parseTree(donated_node) + " at location " + str(node_2))
        #    #we are going to want to copy this tree before we stick stuff into it, in case we want to save the parent
        #    new_root = copy_tree(tree2.node)
        #    print("Equation before: " + str(parseTree(new_root)))
        #    replace_node_at_operator_location(new_root, node_1, 0, new_donated_node)
        #    print("Equation after: " + str(parseTree(new_root)))
        #    print()
        #we have finished one iteration of the combination, add to descendents list now
        eq = parseTree(new_root)
        descendants.append(TreeData(new_root, eq, calc_rms_error(eq, file_data)))

    tree_roots.extend(descendants)




if __name__ == "__main__":
    read_file(sys.argv[1])
    create_random_trees()

    for i in range(0, 10):
        if check_for_winner() is True:
            break
        else:
            print("Starting generation " + str(i))
            print_equations(tree_roots)
            produce_next_generation()
            print_equations(tree_roots)

    #print_equations(produce_next_generation())

    #print()
    #print(tree_roots[0].equation)
    #print(count_operator_nodes(tree_roots[0].node, 0))
    #result = get_node_at_operator_location(tree_roots[0].node, 3)
    #print(parseTree(result))

    #copy tree test
    #print()
    #print(tree_roots[0].equation)
    #new_tree = copy_tree(tree_roots[0].node)
    #new_tree.data = '-'
    #print(parseTree(tree_roots[0].node))
    #print(parseTree(new_tree))

    #root = EquationNode('+')
    #root.left = EquationNode('-')
    #root.right = EquationNode('5')
    #root.left.left = EquationNode('7')
    #root.left.left.right = EquationNode('6')
    #new_root = copy_tree(root)
    #print(parseTree(new_root))
    #root.data = '-'
    #print(parseTree(new_root))


