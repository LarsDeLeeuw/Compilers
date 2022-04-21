#===================================================================#
# Name        : test_ass1.py                                        #
# Author      : Lars De Leeuw                                       #
# Date        : 11/03/2022                                          #
# Version     : 0.1                                                 #
# Description : unittest.TestSuite containing all unittest.TestCase #
#               associated with testing the quality, features       #
#               and requirements implemented for assignment 1.      #
#===================================================================#

import xml.etree.ElementTree as ET
from ASTNodes import *


class AST:

    def __init__(self): 
        self.root = None

    def setRoot(self, node):
        self.root = node
    
    def accept(self, visitor):
        node = self.root
        visitor.visit(node)
    
    def save(self, file):
        output = open(file, 'w')
        output.write("<Ast>\n" + self.root.save() + "</Ast>")
        return 0
    
    def load(self, file):
        root = ET.parse(file).getroot()
        ref_dict = {}
        for child in root.findall("./"):
            """Create node objects and stuff them in dict so they can be referenced later"""
            ref_dict[child.findtext("serial")] = self.load_createNode(child.tag, int(child.findtext("serial")))

        assert(type(ref_dict['0']) is ProgNode)
        """First child should be ProgNode"""
        assert(len(root.findall("PROG")) == 1)
        """Expect exactly 1 ProgNode"""
        self.root = ref_dict['0']

        for child in root.findall("./"):
            """Add children, parents and attributes to nodes"""
            node_serial = child.findtext("serial")

            if type(ref_dict[node_serial]) is ProgNode:
                for stat in child.find("STATS"):
                    ref_dict[node_serial].StatementNodes.append(ref_dict[stat.text])
            elif type(ref_dict[node_serial]) is IdNode:
                ref_dict[node_serial].ID = child.findtext('id')

                ref_dict[node_serial].PrimitiveNode = ref_dict[child.findtext('primitive')]
                ref_dict[node_serial].PrimitiveNode.Parent = ref_dict[node_serial]

                ref_dict[node_serial].ExpressionNode = ref_dict[child.findtext('expression')]
                ref_dict[node_serial].ExpressionNode.Parent = ref_dict[node_serial]
            elif type(ref_dict[node_serial]) is BinaryExpressionNode:
                ref_dict[node_serial].lhs = ref_dict[child.findtext('lhs')]
                ref_dict[node_serial].lhs.Parent = ref_dict[node_serial]

                ref_dict[node_serial].op = ref_dict[child.findtext('op')]
                ref_dict[node_serial].op.Parent = ref_dict[node_serial]

                ref_dict[node_serial].rhs = ref_dict[child.findtext('rhs')]
                ref_dict[node_serial].rhs.Parent = ref_dict[node_serial]
            elif type(ref_dict[node_serial]) is IntegerNode:
                ref_dict[node_serial].value = int(child.findtext('value'))
            elif type(ref_dict[node_serial]) is FloatNode:
                ref_dict[node_serial].value = float(child.findtext('value'))  
            elif type(ref_dict[node_serial]) is CharNode:
                ref_dict[node_serial].value = str(child.findtext('value'))
            else:
                pass
        return 0
    
    def load_createNode(self, tag, serial):
        """Helper method for loading, had to put switcher in different method because
            otherwise only one of each node can exist some weird python behavior"""
        switcher = {
            "PROG" : ProgNode(),
            "IDNODE" : IdNode(),
            "PRIMINTNODE" : PrimitiveIntNode(),
            "PRIMFLOATNODE" : PrimitiveFloatNode(),
            "PRIMCHARNODE" : PrimitiveCharNode(),
            "BINOPNODE" : BinaryExpressionNode(),
            "ADDNODE" : AdditionNode(),
            "SUBNODE" : SubstractionNode(),
            "MULNODE" : MultiplicationNode(),
            "DIVNODE" : DivisionNode(),
            "LSTNODE" : LessThanNode(),
            "GRTNODE" : GreaterThanNode(),
            "EQNODE"  : IsEqualNode(),
            "NEQNODE" : IsNotEqualNode(),
            "LEQNODE" : LessOrEqualNode(),
            "GEQNODE" : GreaterOrEqualNode(),
            "ANDNODE" : AndNode(),
            "ORNODE"  : OrNode(),
            "MODNODE" : ModulusNode(),
            "INTNODE" : IntegerNode(),
            "FLOATNODE" : FloatNode(),
            "CHARNODE" : CharNode()
        }

        node = switcher.get(tag, AbstractNode())
        node.serial = serial
        return node