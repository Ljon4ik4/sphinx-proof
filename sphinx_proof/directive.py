"""
sphinx_proof.directive
~~~~~~~~~~~~~~~~~~~~~~

A custom Sphinx Directive

:copyright: Copyright 2020 by the QuantEcon team, see AUTHORS
:licences: see LICENSE for details
"""

from typing import List
from docutils import nodes
from docutils.nodes import Node
from sphinx.util import logging
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

MESSAGE_CATALOG_NAME = "proof"
from sphinx.locale import get_translation
_ = get_translation(MESSAGE_CATALOG_NAME)

from docutils.statemachine import ViewList

import os
from pathlib import Path


from .node_generator import NODE_TYPES, unenumerable_node, headless_node

logger = logging.getLogger(__name__)


class ElementDirective(SphinxDirective):
    """A custom Sphinx Directive"""

    name = ""
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "label": directives.unchanged_required,
        "class": directives.class_option,
        "nonumber": directives.flag,
    }

    def run(self) -> List[Node]:
        env = self.env
        HEADERLESS_TYPE_LIST=env.config.headerless_type_list
        NONUMBER_TYPE_LIST=env.config.nonumber_type_list
        
        if not hasattr(env, "proof_list"):
            env.proof_list = {}

        realtyp = self.name.split(":")[1]
        countertyp = realtyp
        if env.config.proof_uniform_numbering:
            countertyp = "theorem"

        classes, class_name = ["proof_env", realtyp], self.options.get("class", [])
        if class_name:
            classes.extend(class_name)

        serial_no = env.new_serialno()
        label = self.options.get("label", "")
        if label:
            self.options["noindex"] = False
            node_id = f"{label}"
        else:
            self.options["noindex"] = True
            label = f"{realtyp}-{serial_no}"
            node_id = f"{realtyp}-{serial_no}"
        ids = [node_id]

        # Duplicate label warning
        if not label == "" and label in env.proof_list.keys():
            #path = env.doc2path(env.docname)[:-3] sphinx 9 deprecation warning, so:
            path = Path(self.env.doc2path(env.docname))
            location = os.fspath(path.with_suffix(""))
            other_path = env.doc2path(env.proof_list[label]["docname"])
            msg = f"duplicate {realtyp} label '{label}', other instance in {other_path}"
            logger.warning(msg, location=location, color="red")

        title_text = ""
        if (self.arguments != []):
            title_text += f" ({self.arguments[0]})"
        #this compiles the title text into nodes
        textnodes, messages = self.state.inline_text(title_text, self.lineno)

        not_enumerable = ("nonumber" in self.options) or (realtyp in NONUMBER_TYPE_LIST) or realtyp in HEADERLESS_TYPE_LIST

        if realtyp in HEADERLESS_TYPE_LIST:
            node = headless_node()
            pass
        elif not_enumerable:
            node = unenumerable_node()
        else:
            node_type = NODE_TYPES[countertyp]
            node = node_type()

        node.document = self.state.document

        content = ViewList() # Modifying self.content causes a strange bug in the latex output, so creating a copy
        for i, line in enumerate(self.content):
            content.append(line, self.state.document.current_source, self.lineno)

        section = None
        if realtyp in HEADERLESS_TYPE_LIST:
            section = nodes.admonition(classes=classes)
            if self.arguments:
                arg = self.arguments[0]
                content.insert(0, arg, self.state.document.current_source, self.lineno)
                content.insert(1, "", self.state.document.current_source, self.lineno)
            content[0] = "{}. ".format((realtyp.title())) + content[0]
        else:
            node += nodes.title(title_text, "", *textnodes)
            section = nodes.section(classes=[f"{realtyp}-content"], ids=["proof-env-content"])
        
        self.state.nested_parse(content, self.content_offset, section)

        node += section

        
        # Set node attributes
        node["ids"].extend(ids)
        node["classes"].extend(classes)
        node["title"] = title_text
        node["label"] = label
        node["countertype"] = countertyp
        node["realtype"] = realtyp
        node["nonumber"] = not_enumerable
        if not realtyp in HEADERLESS_TYPE_LIST:
            env.proof_list[label] = {
                "docname": env.docname,
                "countertype": countertyp,
                "realtype": realtyp,
                "ids": ids,
                "label": label,
                "prio": 0,
                "nonumber": not_enumerable,
            }
        return [node]
