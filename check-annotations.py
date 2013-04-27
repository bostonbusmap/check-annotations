import argparse
import os
import os.path

from logilab.astng import builder
from logilab.astng.utils import ASTWalker
from logilab.astng.scoped_nodes import Module

abuilder = builder.ASTNGBuilder()

def make_paths(path) -> list:
    """returns a collection of python file paths"""

    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    yield os.path.join(root, file)
    else:
        raise Exception("%s is not a directory or a file" % path)

class PrintAll:
    def set_context(self, node, child_node):
        pass

    def visit_module(self, node):
        print(node.as_string())

def print_module(path):
    print("In path %s" % path)
    with open(path) as f:
        code = f.read()
    obj = abuilder.string_build(code)
    ASTWalker(PrintAll()).walk(obj)


def main():
    parser = argparse.ArgumentParser(description='Statically check types for consistency')
    parser.add_argument('path', type=str, help='path to directory containing Python files,'
                                               ' or a path to a single Python file')
    parser.add_argument("--print", action='store_true')
    args = parser.parse_args()

    paths = make_paths(args.path)
    if args.print:
        for path in paths:
            print_module(path)

if __name__ == "__main__":
    main()