import ast
from _ast import AST
import graphviz

with open('fibonacci.py', 'r') as f:
    code = f.read()


class Tree:
    tree_id_counter = 0  # static

    def __init__(self):
        self.children = []
        self.data = {'name': '', 'type': '', 'node_obj': None}
        self.tree_id = str(Tree.tree_id_counter)
        Tree.tree_id_counter += 1

    def append(self, val):
        self.children.append(val)


class GraphCreator:
    """
    class that builds and shows tree-graph
    """
    def __init__(self, filename):
        self.graph = graphviz.Digraph(filename=filename)

    def get_label(self, tree):
        """
        label to be shown on graph
        """
        name = tree.data['name']
        type_ = tree.data['type']
        node_obj = tree.data["node_obj"]
        # node stands for variable/const and its name/value is needed
        if type_ == 'Name':
            type_ += f': {node_obj.id}'
        if type_ == 'arg':
            type_ += f': {node_obj.arg}'
        if type_ == 'Constant':
            type_ += f': {node_obj.value}'

        if name:
            if type_:
                return f'{name}:\n{type_}'
            return name
        return type_

    def get_color(self, tree):
        """
        selects color depending on the type of node
        """
        name = tree.data['name']
        type_ = tree.data['type']
        colors_by_type = {
            # vars and constants
            'Constant': 'darkorange',
            'Name': 'orange',
            'arg': 'orange',
            # operators
            'BinOp': 'pink',
            'Eq': 'red',
            'Assign': 'orchid',
            # other
            'If': 'green',
            'For': 'green',
            'Return': 'dodgerblue',
            'Subscript': 'hotpink'
        }
        colors_by_name = {
            'func': 'deeppink',
            # operators
            'ops': 'pink',
            'op': 'red'
        }
        if name in colors_by_name:
            return colors_by_name[name]
        if type_ in colors_by_type:
            return colors_by_type[type_]
        if not len(tree.children):
            return 'dimgrey'
        return 'lightgrey'

    def add_to_graph(self, tree):
        """
        add to graph tree's nodes and edges between father and child nodes
        """
        label = self.get_label(tree)
        color = self.get_color(tree)
        self.graph.node(tree.tree_id, label=label, style='filled', color=color)

        for child in tree.children:
            self.graph.edge(tree.tree_id, child.tree_id)
            self.add_to_graph(child)

    def view(self):
        """
        creates pdf file for graph and launches it
        """
        self.graph.view()


class Visitor(ast.NodeVisitor):
    """
    class that visits AST's nodes and saves info about them into a tree structure
    """
    def generic_visit(self, node):
        """
        actions, when Visitor visits the node
        """
        tree = Tree()
        tree.data['type'] = type(node).__name__
        tree.data['node_obj'] = node
        for field, value in ast.iter_fields(node):
            if field == 'ctx':  # this stands for loading variable and is not needed
                continue
            if isinstance(value, list):
                child_tree = Tree()
                child_tree.data['name'] = field
                for item in value:
                    if isinstance(item, AST):
                        child_tree.append(self.visit(item))
                tree.append(child_tree)
            elif isinstance(value, AST):
                subtree = self.visit(value)
                if subtree is not None:
                    subtree.data['name'] = field
                tree.append(subtree)
        return tree


def main():
    ast_obj = ast.parse(code)
    vis = Visitor()
    tree = vis.visit(ast_obj)

    # tree.print()
    graph = GraphCreator('images/ast')
    graph.add_to_graph(tree)
    graph.view()


if __name__ == "__main__":
    main()
