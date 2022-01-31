import ast
from _ast import AST
import graphviz

with open('fibonacci.py', 'r') as f:
    code = f.read()


class Tree:
    tree_id_counter = 0  # static

    def __init__(self):
        self.children = []
        self.data = {'name': '', 'type': '', 'code': '', 'node': None, 'node_obj': None}
        self.tree_id = str(Tree.tree_id_counter)
        Tree.tree_id_counter += 1

    def print(self, n=0):
        print(
            f"{n}. name: {self.data['name']}, type: {self.data['type']}, code: {self.data['code']}, node: {self.data['node']}")
        for node in self.children:
            if node is not None:
                node.print(n + 1)

    def append(self, val):
        self.children.append(val)

    def add_to_graph(self, graph):
        label = self.get_label()
        graph.node(self.tree_id, label=label)

        for child in self.children:
            graph.edge(self.tree_id, child.tree_id)
            child.add_to_graph(graph)

    def calc_color(self):
        pass

    def get_label(self):
        name = self.data['name']
        type_ = self.data['type']
        node_obj = self.data["node_obj"]
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


class v(ast.NodeVisitor):
    def generic_visit(self, node):
        tree = Tree()
        tree.data['type'] = type(node).__name__
        tree.data['code'] = ast.unparse(node)
        tree.data['node'] = ast.dump(node)
        tree.data['node_obj'] = node
        for field, value in ast.iter_fields(node):
            if field == 'ctx':
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

    def visit_Load(self, node):
        return None


def main():
    ast_obj = ast.parse(code)
    vis = v()
    tree = vis.visit(ast_obj)
    tree.print()
    g = graphviz.Digraph('ast', filename='images/ast')
    tree.add_to_graph(g)
    g.view()


if __name__ == "__main__":
    main()

colors = {
    'Const': 'cyan',
    'Name': 'orange',

}
