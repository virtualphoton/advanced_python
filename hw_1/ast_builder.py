import ast
from _ast import AST
import graphviz

with open('fibonacci.py', 'r') as f:
    code = f.read()


class Tree:
    tree_id_counter = 0  # static

    def __init__(self):
        self.children = []
        self.data = None
        self.tree_id = str(Tree.tree_id_counter)
        Tree.tree_id_counter += 1

    def print(self, n=0):
        self.data['name'] = self.data.get('name', '')
        self.data['type'] = self.data.get('type', '')
        self.data['code'] = self.data.get('code', '')
        print(f"{n}. name: {self.data['name']}, type: {self.data['type']}, code: {self.data['code']}")
        for node in self.children:
            if node is not None:
                node.print(n + 1)

    def append(self, val):
        self.children.append(val)

    def add_to_graph(self, graph):
        label = self.data['name']
        graph.node(self.tree_id, label=label)

        for child in self.children:
            graph.edge(self.tree_id, child.tree_id)
            child.add_to_graph(graph)

    def calc_color(self):
        pass


class v(ast.NodeVisitor):
    def generic_visit(self, node):
        tree = Tree()
        tree.data = {"type": type(node).__name__, "code": ast.unparse(node), 'node': node}
        for field, value in ast.iter_fields(node):
            if field == 'ctx':
                continue
            if isinstance(value, list):
                child_tree = Tree()
                child_tree.data = {'name': field}
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
