
class quad(object):
    def __init__(self):
        self.quads = []
        self.poper = []
        self.op_stack = []
        self.type_stack = []
        self.jump_stack = []
        self.counter = 0

    def generate_quad(self, op, left, right, t):
        q = [op, left, right, t]
        self.quads.append(q)
        self.counter += 1