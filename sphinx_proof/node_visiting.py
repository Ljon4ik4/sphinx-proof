"""
sphinx_proof.node_visiting
~~~~~~~~~~~~~~~~~~

Enumerable and unenumerable nodes

:copyright: Copyright 2020 by the QuantEcon team, see AUTHORS
:licences: see LICENSE for details
"""

from docutils import nodes
from docutils.nodes import Node
from sphinx.writers.latex import LaTeXTranslator
from sphinx.locale import get_translation


from sphinx.util import logging

logger = logging.getLogger(__name__)

MESSAGE_CATALOG_NAME = "proof"
_ = get_translation(MESSAGE_CATALOG_NAME)

CR = "\n"
latex_admonition_start = CR + "\\begin{sphinxadmonition}{note}"
latex_admonition_end = "\\end{sphinxadmonition}" + CR

def do_nothing(self, node: Node) -> None:
    pass

def visit_node_html(self, node: Node) -> None:
    self.body.append(self.starttag(node, "div", CLASS="admonition"))

def visit_node_latex(self, node: Node) -> None:
    docname = find_parent(self.builder.env, node, "section")
    self.body.append("\\label{" + f"{docname}:{node.attributes['label']}" + "}")
    self.body.append(latex_admonition_start)

def depart_node_latex(self, node: Node) -> None: 
    countertyp = node.attributes.get("countertype", "")
    realtyp = node.attributes.get("realtype", "")
    number_str = ""
    if not node.attributes.get("nonumber", False):
        number = get_node_number(self, node, countertyp)
        number_str = f" {number}"
    idx = list_rindex(self.body, latex_admonition_start) + 2
    self.body.insert(idx, f"{realtyp.title()}{number_str}")
    self.body.append(latex_admonition_end)


def depart_node_html(self, node: Node) -> None:
    countertyp = node.attributes.get("countertype", "")
    realtyp = node.attributes.get("realtype", "")
    title = node.attributes.get("title", "")

    if not node.attributes.get("nonumber", False):
        number = get_node_number(self, node, countertyp)
        element = f"{_(realtyp.title())} {number} "
        idx = self.body.index(f"{countertyp} {number} ")
        self.body[idx] = element
    else: 
        element =  f"<span>{_(realtyp.title())} </span>"
        if title == "":
            logger.warning(element)
            idx = list_rindex(self.body, '<p class="admonition-title">') + 1
        else:
            idx = list_rindex(self.body, title)
        self.body.insert(idx, element)
    self.body.append("</div>")


def get_node_number(self, node: Node, countertyp) -> str:
    """Get the number for the directive node for HTML."""
    ids = node.attributes.get("ids", [])[0]
    key = countertyp
    if isinstance(self, LaTeXTranslator):
        docname = find_parent(self.builder.env, node, "section")
        fignumbers = self.builder.env.toc_fignumbers.get(
            docname, {}
        )  # Latex does not have builder.fignumbers
    else:
        fignumbers = self.builder.fignumbers
        if self.builder.name == "singlehtml":
            key = "%s/%s" % (self.docnames[-1], countertyp)
    number = fignumbers.get(key, {}).get(ids, ())
    return ".".join(map(str, number))


def find_parent(env, node, parent_tag):
    """Find the nearest parent node with the given tagname."""
    while True:
        node = node.parent
        if node is None:
            return None
        # parent should be a document in toc
        if (
            "docname" in node.attributes
            and env.titles[node.attributes["docname"]].astext().lower()
            in node.attributes["names"]
        ):
            return node.attributes["docname"]

    if node.tagname == parent_tag:
        return node.attributes["docname"]

    return None


def list_rindex(li, x) -> int:
    """Getting the last occurence of an item in a list."""
    for i in reversed(range(len(li))):
        if li[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))