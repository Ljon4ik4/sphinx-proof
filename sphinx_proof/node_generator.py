from docutils import nodes
from docutils.nodes import Node
import sys

PROOF_TYPE_LIST = [
    "axiom",
    "theorem",
    "lemma",
    "algorithm",
    "definition",
    "remark",
    "conjecture",
    "corollary",
    "criterion",
    "example",
    "property",
    "observation",
    "proposition",
    "assumption",
    "notation",
    "proof",
]

DEFAULT_NONUMBER_TYPE_LIST = [
    "proof",
]

DEFAULT_HEADERLESS_TYPE_LIST = [
    "proof",
]


def create_node_class(name_prefix):
    class_name = f"{name_prefix}_node"
    # Create the class dynamically
    new_class = type(class_name, (nodes.Admonition, nodes.Element), {})
    module = sys.modules[__name__]
    new_class.__module__ = module.__name__
    setattr(module, class_name, new_class)
    return new_class

def create_nodes(lst):
    return {item: create_node_class(item) for item in lst}

NODE_TYPES = create_nodes(PROOF_TYPE_LIST)

class unenumerable_node(nodes.Admonition, nodes.Element):
    pass

class headless_node(nodes.Admonition, nodes.Element):
    pass