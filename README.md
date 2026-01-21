# sphinx-proof

[![Documentation Status][rtd-badge]][rtd-link]
[![Github-CI][github-ci]][github-link]
[![Coverage Status][codecov-badge]][codecov-link]
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/executablebooks/sphinx-proof/main.svg)](https://results.pre-commit.ci/latest/github/executablebooks/sphinx-proof/main)


## Rewrite

### New features

This branch contains a significantly rewritten version.
New features added:
- one can choose between numbering per-proof-type and uniform numbering via `proof_uniform_numbering`
- one can manage a list of types which have no number by default (usually only proof) via `nonumber_type_list`
- one can manage a list of types which are headless (no admonition title) by default (usually only proof) `headless_type_list`

This potentially/ partially answers the issues
- [86](https://github.com/executablebooks/sphinx-proof/issues/86)
- [64](https://github.com/executablebooks/sphinx-proof/issues/64)


### Disclaimer

I tried doing this (with an automated coding assistance employed on individual lines) and without a deep understanding how sphinx works, so be cautious. I am sure none of the changes are 'malicious' and it now passes the tests, but that's all I can say....


### Under the hood

- I tried changing the naming of things to be more self-explanatory, so less things are called 'proof' now in the codebase,

- the classes that are necessary are now automatically generated from a list. This makes creating new theorem-kinds easier. (change necessary just in one file `node_generator.py` and potentially in the css files for custom design).

- It should now be easy to add the possibility for custom environment types, one simply needs to create some dummy ones e.g. "dummy1",...,"dummy13" to the `PROOF_TYPE_LIST` in `node_generator.py` and add some programming logic in `directive.py` so map certain `realtypes` to these `countertypes`. (This could be done by allowing users to provide a dictionary for the mapping and then using that. Such a dictionary could be `{"challenge" : "dummy1", ...}`).

- By the same method it should be possible to have more advanced counting setup (e.g. one counter for defs , one for lemmas, theorems, propositions, one for axioms).

### Missing things

- localization to translate the word proof is missing
- the documentation has not been systematically adapted
- css styling might differ a little from the previous one and could also be improved 
- only existing tests were adapted, no new tests were created
- Maybe there is a way to add no-number to all envs of a certain kind directly in sphinx, that would make the corresponding option (`nonumber_type_list`) useless and then it should be removed.


**A proof extension for Sphinx**.

This package contains a [Sphinx](http://www.sphinx-doc.org/) extension
for producing proof, theorem, axiom, lemma, definition, criterion, remark, conjecture,
corollary, algorithm, example, property, observation, proposition and assumption directives.

## Features

- **15 directive types** for mathematical proofs and theorems
- **Automatic numbering** of directives
- **Cross-referencing** support via `prf:ref` role
- **33 languages supported** - Complete translations for all directive types in English plus 32 additional languages (Arabic, Bengali, Bulgarian, Chinese, Czech, Danish, Dutch, Finnish, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Swedish, Thai, Turkish, Ukrainian, Urdu, Vietnamese)
- **Customizable styling** with multiple theme options


## Get started

To get started with `sphinx-proof`, first install it through `pip`:

```
pip install sphinx-proof
```

then, add `sphinx_proof` to your sphinx `extensions` in the `conf.py`

```python
...
extensions = ["sphinx_proof"]
...
```


## Documentation

See the [Sphinx Proof documentation](https://sphinx-proof.readthedocs.io/en/latest/) for more information.


## Contributing

We welcome all contributions! See the [EBP Contributing Guide](https://executablebooks.org/en/latest/contributing.html) for general details, and below for guidance specific to sphinx-proof.


[rtd-badge]: https://readthedocs.org/projects/sphinx-proof/badge/?version=latest
[rtd-link]: https://sphinx-proof.readthedocs.io/en/latest/?badge=latest
[github-ci]: https://github.com/executablebooks/sphinx-proof/workflows/continuous-integration/badge.svg?branch=main
[github-link]: https://github.com/executablebooks/sphinx-proof/actions/workflows/ci.yml
[codecov-badge]: https://codecov.io/gh/executablebooks/sphinx-proof/branch/main/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/sphinx-proof
