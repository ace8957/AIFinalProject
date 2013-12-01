import os
import sys
import math

operators = ['+', '-', '*', '/', 'sin', '^']
test_data = []

class EquationNode:
    eq = ''
    def __init__(self, data, left=None, right=None):
        if data in operators:
            self.left = left
            self.right = right
        self.data = data

    def parseTree(self):
        #if isinstance(self.left,EquationNode):
        if self.left in operators:
            self.parseTree(self.left)
        self.eq += self.left
        self.eq += self.data
        #if isinstance(self.right,EquationNode):
        if self.right in operators:
            self.parseTree(self.right)
        self.eq += self.right
        print(self.eq)
        print(eval(self.eq))


def read_file(filename):
    f = open(filename, 'r')
    line = f.readline()
    if line != '':
        test_data.append(line.replace('\n',''))
    while line != '':
        line = f.readline()
        if line != '':
            test_data.append(line.replace('\n',''))

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
    root = EquationNode('+', '4', '5')
    root.parseTree()
    read_file(sys.argv[1])
    calc_rms_error('x+2', ['2,3','4,5'])
