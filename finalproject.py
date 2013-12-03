import os
import sys
from math import sin
import random

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

    def parseTree(self):
        #if isinstance(self.left,EquationNode):
        if self.left in operators:
            self.parseTree(self.left)
        self.eq += str(self.left.data)
        self.eq += str(self.data)
        #if isinstance(self.right,EquationNode):
        if self.right in operators:
            self.parseTree(self.right)
        self.eq += str(self.right.data)
        print(self.eq)
        print(eval(self.eq))

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
                print("Assigning " + str(left) + " to left node at depth " + str(current_depth))
                current_node.left = EquationNode(left)
                assign_node_values(current_node.left,current_depth+1,need_x,max_depth)
            if right is not None:
                right = random.choice(possible_values)
                if right == 'num':
                    right = random.randrange(0,100)
                elif left == 'x':
                    need_x = False
                print("Assigning " + str(right) + " to right node at depth " + str(current_depth))
                current_node.right = EquationNode(right)
                assign_node_values(current_node.right,current_depth+1,need_x,max_depth)


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
        try:
            ans = eval(equation.replace('x', str(x)))
        except ZeroDivisionError:
            return 9999999999
        except OverflowError:
            return 9999999999
        try:
            squares.append((y-ans)**2)
        except OverflowError:
            return 9999999999
    ssum = 0
    for square in squares:
        ssum += square
    try:
        ssum = ssum / len(squares)
    except OverflowError:
            return 9999999999
    return ssum ** 0.5


def create_random_trees():
    for x in range(0,20):
        node = EquationNode(random.choice(operators))
        assign_node_values(node, 0, True, 4)
        eq = parseTree(node)
        tree_roots.append(TreeData(node, eq, calc_rms_error(eq, file_data)))
        print()


def print_equations(tree):
    for node in tree:
        print(node.error)

if __name__ == "__main__":

    read_file(sys.argv[1])
    create_random_trees()
    print_equations(tree_roots)
    print()
    sorted_tree = sorted(tree_roots, key=lambda node: node.error)
    print_equations(sorted_tree)

