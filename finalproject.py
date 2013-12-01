import os
import sys
import math
import random

operators = ['+', '-', '*', '/', 'sin', '^']
file_data = []
tree_roots = []
equations = []

#class EquationNode:
#    eq = ''
#    def __init__(self, data, left=None, right=None):
#        if data in operators:
#            self.left = left
#            self.right = right
#        self.data = data
#
#    def parseTree(self):
#        #if isinstance(self.left,EquationNode):
#        if self.left in operators:
#            self.parseTree(self.left)
#        self.eq += self.left
#        self.eq += self.data
#        #if isinstance(self.right,EquationNode):
#        if self.right in operators:
#            self.parseTree(self.right)
#        self.eq += self.right
#        print(self.eq)
#        print(eval(self.eq))

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


#def generate_random_equation():
#    max_depth = random.randrange(4)
#    #Everything will be denoted by parentheses.

#This will need to be called recursively
def assign_node_values(current_node, current_depth, need_x, max_depth):
            left = 0
            right = 0
            double_operators = ['+', '-', '*', '/', '^']
            single_operators = ['sin']
            possible_values = ['+', '-', '*', '/', 'sin', '^', 'num', 'x','num','num']

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
                    left = random.randrange(0,100)
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


#def construct_random_trees():
#    double_operators = ['+', '-', '*', '/', '^']
#    single_operators = ['sin']
#    #we will create twenty starting trees to use for genetic evolution
#    for i in range(0,20):
#        #find the max depth of the tree that we will use. Does this need to always be 4(max)?
#        max_depth = random.randrange(0,4)
#        need_x = True
#        root = None
#        last_root = None
#        remaining_nodes = []
#        for j in range(0,max_depth+1):
#            #the values which will go into the left and right nodes
#            left = 0
#            right = 0
#            #decide what the first operator should be
#            op = random.choice(operators)
#            #if the operator is in the single_operators list, we will not have a left or right node
#            if op in single_operators:
#                #will the single leg be on the left or right?
#                leg = random.choice(['left', 'right'])
#                if leg == 'left':
#                    right = None
#                elif leg == 'right':
#                    left = None
#            #check to see if we are at our maximum depth
#            if j == max_depth:
#                if need_x is True:
#                    if left == 0:
#                        left = 'x'
#                        need_x = False
#                    elif right == 0:
#                        right = 'x'
#                        need_x = False
#                else:
#                    #we do not still need to place an x, and we are at max depth, so pick a random number
#                    if left == 0:
#                        left = random.randrange(0,100)
#                    if right == 0:
#                        right = random.randrange(0,100)
#            else:
#                #check to see if we are the root node, if we are, set root to the current node
#                # and last_node to the current node


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
        ans = eval(equation.replace('x', str(x)))
        squares.append((y-ans)**2)
    ssum = 0
    for square in squares:
        ssum += square
    ssum = ssum / len(squares)
    return ssum ** 0.5

if __name__ == "__main__":
    #root = EquationNode('+')
    #left = EquationNode(4)
    #right = EquationNode(5)
    #root.left = left
    #root.right = right

    root = EquationNode('+')
    assign_node_values(root, 0, True, 4)
    root.parseTree()


    read_file(sys.argv[1])
    calc_rms_error('x+2', ['2,3','4,5'])
