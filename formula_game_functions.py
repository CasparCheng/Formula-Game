"""
# Copyright Nick Cheng, Jiyuan Cheng 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.


def validation_1(formula, index, length):
    '''(int) -> tuple of (FormulaTree, int)
    Given a formula, a index and the length the function check whether
    it is valid recursively. Then build it as formulatree, return the tuple of
    formula tree and its index if it is valid, otherwise, return None

    >>> formula = "x+(-y)"
    >>> index = 0
    >>> length = 6
    >>> validation_1(formula, index, length)
    None
    >>> formula = "-----a"
    >>> index = 0
    >>> length = 6
    >>> validation_1(formula, index, length)
    NotTree(NotTree(NotTree(NotTree(NotTree(Leaf('a'))))))
    >>> formula = "x"
    >>> index = 0
    >>> length = 1
    >>> validation_1(formula, index, length)
    Leaf('x')
    >>> formula = "-y"
    >>> index = 0
    >>> length = 2
    >>> validation_1(formula, index, length)
    NotTree((Leaf('y'))
    '''
    # define a result which equal to None
    result = None
    # if the it is not the end of formula according to the index
    if index != length:
        # get the letter of the string in the index
        ch = formula[index]
        # check whether it is in lower letters
        if ch in 'abcdefghijklmnopqrstuvwxyz':
            # if it is build it as leaf, and continuethe index for checking
            result = Leaf(ch), index + 1
        # else if the letter of string in the index is the left bracket
        elif ch == '(':
            # call the validation2 function to check whether the stuff in the
            # brackets is valid
            ret = validation_2(formula, index + 1, length)
            # if it is valid
            if ret is not None:
                # get the tuple of the operand and the index
                operand, index = ret
                # if it is not the end of formula
                if index != length:
                    # if the letter of string in the index is right bracket
                    if formula[index] == ')':
                        # get the operand and continue index for checking
                        result = operand, index + 1
        # else if letter of string in the index is "-"
        elif ch == '-':
            # recurse the validation1 for checking whether the stuff is valid
            # after the "-" symbol
            ret = validation_1(formula, index + 1, length)
            # if it is valid
            if ret is not None:
                # get the tuple of operand and the index
                operand, index = ret
                # build the operand as not tree and make tuple with
                # current index
                result = NotTree(operand), index

    return result


def validation_2(formula, index, length):
    '''(int) -> tuple of (FormulaTree, int)
    Given a formula, a index and the length the function check whether
    it is valid in parentheses.
    Return the tuple of formula tree and the index if it is valid
    otherwise return None

    REQ: formula is not empty string

    >>> formula = "(x*y)"
    >>> index = 0
    >>> length = 5
    >>> validation_2(formula, index, length)
    AndTree(Leaf('x'), Leaf('y'))
    >>> formula = "(x+-----y)"
    >>> index = 0
    >>> length = 10
    >>> validation_2(formula, index, length)
    "OrTree(Leaf('x'), NotTree(NotTree(NotTree(NotTree(NotTree(Leaf('y')))))))"
    >>> formula = "(+x*+-z)"
    >>> index = 0
    >>> length = 8
    >>> validation_2(formula, index, length)
    None
    '''
    # define the result which is None
    result = None
    # if it is not the end of formula at that index
    if index != length:
        # call teh validtion1 to check whether is valid
        ret = validation_1(formula, index, length)
        # if it is valid
        if ret is not None:
            # get the tuple of operand and index
            operand_l, index = ret
            # if it is not the end of formula
            if index != length:
                # get the operator at that index
                operator = formula[index]
                # if the operator is "+" or "*"
                if operator in '+*':
                    # call validation1 function to check whether it is valid
                    ret = validation_1(formula, index + 1, length)
                    # if it is valid
                    if ret is not None:
                        # get the operand and the index
                        operator_r, index = ret
                        # if the operator is "+"
                        if operator == '+':
                            # build the OrTree for this and make tuple
                            # with current index
                            result = OrTree(operand_l, operator_r), index
                        # otherwise
                        else:
                            # build the AndTree for this and make tuple
                            # with current index
                            result = AndTree(operand_l, operator_r), index

    return result


def build_tree(formula):
    '''(str) -> FormulaTree
    Given a string of formula, the function build the formula as a tree if it
    is valid.
    Return the formula tree

    REQ: formula is not an empty string

    >>> formula = "x+(-y)"
    >>> index = 0
    >>> length = 6
    >>> build_tree(formula, index, length)
    None
    >>> formula = "-----a"
    >>> index = 0
    >>> length = 6
    >>> build_tree(formula, index, length)
    NotTree(NotTree(NotTree(NotTree(NotTree(Leaf('a'))))))
    >>> formula = "x"
    >>> index = 0
    >>> length = 1
    >>> build_tree(formula, index, length)
    Leaf('x')
    >>> formula = "-y"
    >>> index = 0
    >>> length = 2
    >>> build_tree(formula, index, length)
    NotTree((Leaf('y'))
    '''
    # get the length of inputted formula
    length = len(formula)
    # call teh validation1 function to check whether it is valid and build tree
    ret = validation_1(formula, 0, length)
    # if it is valid
    if ret is not None:
        # get the tuple of operand and the index
        operand, index = ret
        # if the index already is the end of formula
        if index == length:
            # return the operand which is the root
            return operand


def draw_helper(root, indent, indent_1):
    '''(Formula, int, int) -> str
    Given a root of formula tree, and two indentation, the function
    draws the forumla tree and put the appropriate indentation.
    return the string of completed form of drawing

    REQ: root is not None

    >>> formula = "(x+y)"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '+ y\n  x'
    >>> formula = "(x*y)"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '* y\n  x'
    >>> formula = "((x*y)+(z*x))"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '+ * x\n    z\n  * y\n    x'
    '''
    # define result which is None
    result = None
    # create the space accoring to the indentation and add the symbol
    rep = ' ' * (indent_1 if indent == 0 else indent) + root.symbol
    # get the children of root
    children = root.children
    # get the number of children
    length = len(children)
    # if it does not has any children
    if length == 0:
        # just change the line
        result = rep + '\n'
    # else if it has only one child
    elif length == 1:
        # recurse the draw helper function to change
        # the indentation for drawing
        result = rep + draw_helper(children[0], 1, indent_1 + 2)
    # otherwise
    else:
        # recurse the draw helper function twice to change the indentation
        # for drawing the formula tree
        result = rep + draw_helper(children[1], 1, indent_1 + 2) + \
            draw_helper(children[0], 0, indent_1 + 2)

    return result


def draw_formula_tree(root):
    '''(FormulaTree) -> str
    Given a root of a formula tree, the function draws the formula tree
    Return the string which represents the formula tree

    REQ: root is not None

    >>> formula = "(x+y)"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '+ y\n  x'
    >>> formula = "(x*y)"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '* y\n  x'
    >>> formula = "((x*y)+(z*x))"
    >>> root = build_tree(formula)
    >>> indent = 0
    >>> indent_1 = 0
    >>> draw_helper(root, indent, indent_1)
    '+ * x\n    z\n  * y\n    x'
    '''
    # call helper function to draw the formula tree, and return it
    return draw_helper(root, 0, 0)[:-1]


def e_helper(root, mapping):
    '''(FormulaTree, dict) -> int
    Given a root of formula tree and the finished mapping between variables
    and values. The function evaluate the formula is True or False.
    Return the truth value, 1 is True, 0 is False

    REQ: Tree is not empty

    >>> formula = "-y"
    >>> root = build_tree(formula)
    >>> mapping = {y:1}
    >>> e_helper(root, mapping)
    0
    >>> formula = "(x*y)"
    >>> root = build_tree(formula)
    >>> mapping = {x:0, y:1}
    >>> e_helper(root, mapping)
    0
    >>> formula = "(x+y)"
    >>> root = build_tree(formula)
    >>> mapping = {x:1, y:0}
    >>> e_helper(root, mapping)
    1
    >>> formula = "((-x+y)+(-y+x))"
    >>> root = build_tree(formula)
    >>> mapping = {x:1, y:1}
    >>> e_helper(root, mapping)
    1
    '''
    # definr the result which is None
    result = None
    # get the root's symbol
    symbol = root.symbol
    # if the symbol is "+"
    if symbol == '+':
        # recure the function to evaluate the left child and right child
        # then get the max number
        result = max(e_helper(root.children[0], mapping),
                     e_helper(root.children[1], mapping))
    # else if the symbol is "*"
    elif symbol == '*':
        # recurse the function to evaluate the left and right child
        # then get the min number
        result = min(e_helper(root.children[0], mapping),
                     e_helper(root.children[1], mapping))
    # else if the symbol is "-"
    elif symbol == '-':
        # recurse the helper to evaluate the only child and using 1 to minus it
        result = 1 - e_helper(root.children[0], mapping)
    # otherwise
    else:
        # symbol is a variable
        # return its value
        result = mapping[symbol]

    return result


def evaluate(root, variables, values):
    ''' (FormulaTree, str, str) -> int
    Given a root of formula tree, variables of this formula and the values
    which match the corresponding variables as the truth values

    REQ: not empty tree

    >>> formula = "-y"
    >>> root = build_tree(formula)
    >>> variables = "y"
    >>> values = "1"
    >>> evaluate(root, variables, values)
    0
    >>> formula = "(x*y)"
    >>> root = build_tree(formula)
    >>> variables = "xy"
    >>> values = "01"
    >>> evaluate(root, variables, values)
    0
    >>> formula = "(x+y)"
    >>> root = build_tree(formula)
    >>> variables = "xy"
    >>> values = "10"
    >>> evaluate(root, variables, values)
    1
    >>> formula = "((-x+y)+(-y+x))"
    >>> root = build_tree(formula)
    >>> variables = "xy"
    >>> values = "10"
    >>> evaluate(root, variables, values)
    1

    '''

    # map variable to value
    mapping = dict(zip(variables, map(int, values)))
    # call the helper dunction and return the truth value
    return e_helper(root, mapping)


def play2win_helper(root, values, variables, length):
    '''(FormulaTree, str, str, int) -> int
    Given a formula tree , two strings of turns and variables and length of
    Variables. the function find the best move which will lead to winning.
    Return the best moving during whose turn.

    REQ: Tree is not empty
    REQ: len(variables) == len(turns)
    REQ: len(variables) <= len(values)

    >>> formula = "(x*(y*z))"
    >>> root = build_tree(formula)
    >>> turns = "AEE"
    >>> variables = "xyz"
    >>> values = ""
    >>> length = 3
    >>> play2win_helper(root, values, variables, length)
    0
    >>> formula = "(x+(y*z))"
    >>> root = build_tree(formula)
    >>> turns = "EAA"
    >>> variables = "xyz"
    >>> values = "1"
    >>> length = 3
    >>> play2win_helper(root, value, variables, length)
    0
    >>> formula = "((-x*y)+(-y*x))"
    >>> root = build_tree(formula)
    >>> turns = "EA"
    >>> variables = "xy"
    >>> values = "10
    >>> length = 2
    >>> play2win_helper(root, value, variables, length)
    1
    '''
    # define result which is None
    result = None
    # if there is still a value which is needed to give
    if len(values) < length:
        # recurse the numbers of trues and falses if next move is 0
        cnt_true0, cnt_false0 = play2win_helper(root, values + '0',
                                                variables, length)
        # recurse numbers of trues and falses if next move is 1
        cnt_true1, cnt_false1 = play2win_helper(root, values + '1',
                                                variables, length)
        # merge results from the two branches
        result = cnt_true0 + cnt_true1, cnt_false0 + cnt_false1
    # otherwise
    else:
        # call the evaluate function for evaluating
        result = (1, 0) if evaluate(root, variables, values) else (0, 1)

    return result


def play2win(root, turns, variables, values):
    '''(FormulaTree, str, str, str) -> int
    Given a formula tree, three strings of turns, variables and values
    the function find the best move which will lead to winning.
    Return the best moving during whose turn. If there is no winning move
    or whatever you choose, it will be winning, return 1 if it is player E's
    turn, return 0 if it is player A's turn.

    REQ: Tree is not empty
    REQ: len(variables) == len(turns)
    REQ: len(variables) <= len(values)

    >>> formula = "(x*(y*z))"
    >>> root = build_tree(formula)
    >>> turns = "AEE"
    >>> variables = "xyz"
    >>> values = ""
    >>> play2win(root, values, variables, length)
    0
    >>> formula = "(x+(y*z))"
    >>> root = build_tree(formula)
    >>> turns = "EAA"
    >>> variables = "xyz"
    >>> values = "1"
    >>> play2win(root, value, variables, length)
    0
    >>> formula = "((-x*y)+(-y*x))"
    >>> root = build_tree(formula)
    >>> turns = "EA"
    >>> variables = "xy"
    >>> values = "10
    >>> play2win(root, value, variables, length)
    1
    '''
    # get the number of given variables
    length = len(variables)
    # recurse the numbers of trues and falses if next move is 0
    cnt_true0, cnt_false0 = play2win_helper(root, values + '0',
                                            variables, length)
    # recurse the numbers of trues and falses if next move is 1
    cnt_true1, cnt_false1 = play2win_helper(root, values + '1',
                                            variables, length)

    # if it is A's turn
    if turns[len(values)] == 'A':
        # if false number for 0 is less than false number for 1, then
        # the best moving should be 1 else moving is 0
        result = 1 if cnt_false0 < cnt_false1 else 0
    # otherwuse
    else:
        # if true number for 0 is greater than true number for 1, then
        # the best movinf should be 0 else moving is 1
        result = 0 if cnt_true0 > cnt_true1 else 1

    return result
