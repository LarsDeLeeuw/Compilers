class STT:

    def __init__(self): 
        self.root = None
    
    def accept(self, visitor):
        node = self.root
        visitor.visit(node)


class STNode:

    def __init__(self):
        self.parent = None
        self.children = []
        self.symbols = {}
    
class STTVisitor:

    def visit(self, node):
        pass