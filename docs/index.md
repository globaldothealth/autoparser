# AutoParser
AutoParser is a tool for semi-automated data parser creation. The package allows you
to generate a new data parser for converting your source data into a new format specified
using a schema file, ready to use with the data transformation tool [adtl](https://adtl.readthedocs.io/en/latest/index.html).

## Key Features
- Data Dictionary Creation: Automatically create a basic data dictionary framework
- Parser Generation: Generate data parsers to match a given schema

## Framework

```{figure} images/flowchart.png
Flowchart showing the inputs (bright blue), outputs (green blocks) and functions
(dashed diamonds) of AutoParser.
```

## Documentation
```{toctree}
---
maxdepth: 2
caption: Contents:
---
self
getting_started/index
usage/data_dict
usage/parser_generation
examples/example
```