
ops = ['+','-','*','/','^']


class OpTree:
    def __init__(self, data, left=None, right=None):
        if data in ops:
            self.left = left
            self.right = right
        self.data = data

    def evalTree(self):
        eq = ''
        if self.left in ops:
            self.left.evalTree()
        eq += str(self.left)
        eq += self.data
        if self.right in ops:
            self.right.evalTree()
        eq += str(self.right)

        print(eq)
        print (eval(eq))


if __name__ == "__main__":
    root = OpTree('+', '4', '/')
    root.right = OpTree(root.right, '9', '3')
    root.evalTree()
