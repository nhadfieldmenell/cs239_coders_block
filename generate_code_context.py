'''
    Generate abstract syntax tree (ast) for the targeted python script,
    Extract every imported library and every function calls from the parsed tree,
    Return a dict containing these information: {API: [...], method_calls: [...]}
'''

import ast
from collections import deque
import pickle

class FuncCallVisitor(ast.NodeVisitor):
    '''
        Helper class for traversing the abstract syntax tree using Depth First Search.
        It helps extract every function calls such as foo.bar() and foo.bar(ok())
    '''
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)

def get_func_calls(tree):
    '''
        Extract every function calls and every library imports by the targeted python script;
        Return object signature:
            {
                'func_calls': [func_call1, func_call2, ...],
                'imports': [impor1, import2, ...]
            }
    '''

    #TODO: extract function definition and class definition
    func_calls = []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        if isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append(module + '.' + alias.name)

    return {
        'func_calls': func_calls,
        'imports': imports
        }

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input .py file', required=True)
    args = parser.parse_args()
    tree = ast.parse(open(args.input).read())
    result = get_func_calls(tree)
    print result
    with open('code_context.pkl', 'wb') as outfile:
        pickle.dump(result, outfile)
