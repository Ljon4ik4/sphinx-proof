"""
sphinx_proof.directive_generator
~~~~~~~~~~~~~~~~~~~~~~~

List of proof-type directives

:copyright: Copyright 2020 by the QuantEcon team, see AUTHORS
:licences: see LICENSE for details
"""

from .directive import ElementDirective
from .node_generator import PROOF_TYPE_LIST
import sys
def create_directive_class(name_prefix):
    class_name = f"{name_prefix}Directive"
    # Create the class dynamically
    new_class = type(class_name, (ElementDirective,), {"name": name_prefix})
    module = sys.modules[__name__]
    new_class.__module__ = module.__name__
    setattr(module, class_name, new_class)
    return new_class

def create_directives(lst):
    return {item: create_directive_class(item) for item in lst}

DIRECTIVE_TYPES = create_directives(PROOF_TYPE_LIST)

