import os
import sys
import math

operators = ['+', '-', '*', '/', 'sin', '^']

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

if __name__ == "__main__":
    root = EquationNode('+', '4', '5S')
    root.parseTree()