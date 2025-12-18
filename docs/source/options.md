# Options

## Minimal color scheme

This package has the option to choose a more **minimal** color scheme.

The aim is to create admonitions that are clearly different to the core text with
colors that do not over emphasises the admonition such as

```{figure} _static/img/definition-minimal.png
```

compared to the current default

```{figure} _static/img/definition.png
```

To enable the `minimal` color scheme you can use the following.

### Jupyter Book Project

Add `proof_minimal_theme = True` to your `_config.yml`

```yaml
sphinx:
  config:
    proof_minimal_theme: true
```

### Sphinx Project

Add `proof_minimal_theme = True` to your `conf.py`


## Shared numbering

By default, each type of theorem has their own numbering and counter.
This can be changed to a common counter by setting the option `proof_uniform_numbering` to true.

### Sphinx Project

Add `proof_uniform_numbering = True` to your `conf.py`


## Types without a number by default

By default only the `prf:proof` is unnumbered. The list of unnumbered types can be set by `nonumber_type_list` 

### Sphinx Project

Add e.g. `nonumber_type_list = ["proof", "example", ...]` to your `conf.py`



## Types without a Title line

By default only the `prf:proof` has no title line. The list of such headless types can be set by `headerless_type_list` 

### Sphinx Project

For instance, if one wants proofs to have a headline, e.g. to make them collapsible, add `nonumber_type_list = []` to your `conf.py`.

```{prf:remark} 
:nonumber:

Anything headless will automatically be unnumbered. (at least in the html output)
```

