# autoparser

**This repository has been archived, as autoparser is now available and being actively developed within ADTL**

autoparser helps in the generation of ADTL parsers as
TOML files, which can then be processed by
[adtl](https://github.com/globaldothealth/adtl) to transform files from the
source schema to a specified schema.

Documentation: [ReadTheDocs](https://autoparser.readthedocs.io/en/latest)

Contains functionality to:
1. Create a basic data dictionary from a raw data file (`create-dict`)
2. Use an LLM (currently via either OpenAI or Google's Gemini) to add descriptions to the 
    data dictionary, to enable better parser auto-generation (`add-descriptions`)
3. Create a mapping csv file linking source to target data fields and value mappings 
    using the LLM, which can be edited by a user (`create-mapping`)
4. Create a TOML parser file ready for use with ADTL, based on a JSON schema
    (rules-based from the mapping file; `create-parser`).

All 4 functions have both a command-line interface, and a python function associated.

## Parser construction process (CLI)

1. **Data**: Get the data as CSV or Excel and the data dictionary if available.

2. **Creating autoparser config**: Optional step if the data is not in REDCap
   (English) format. The autoparser config ([example](src/autoparser/config/redcap-en.toml))
    specifies most of the variable configuration settings for autoparser.

3. **Preparing the data dictionary**: If the data dictionary is not in CSV, or
   split across multiple Excel sheets, then it needs to be combined to a single
   CSV. If a data dictionary does not already exist, one can be created using

   ```shell
    autoparser create-dict <path to data> -o <parser-name>
   ```

   Here, `-o` sets the output name, and will create
   `<parser-name>.csv`. For optional arguments (such as using a custom configuration
   which was created in step 2), see `autoparser create-dict --help`.

4. **Generate intermediate mappings (CSV)**: Run with config and data dictionary
   to generate mappings:

   ```shell
   autoparser create-mapping <path to data dictionary> <path to schema> <language> <api key> -o <parser-name>
   ```

   Here `language` refers to the language of the original data, e.g. "fr" for french 
   language data. `autoparser` defaults to using OpenAI as the LLM API, so the api key 
   provided should be for the OpenAi platform. In future, alternative API's and/or a 
   self-hosted llm are planned to be provided as options.

5. **Curate mappings**: The intermediate mappings must be manually curated, as
   the LLM may have generated false matches, or missed certain fields or value mappings.

6. **Generate TOML**: This step is automated and should produce a TOML file that
   conforms to the parser schema. 

   For example:

   ```shell
   autoparser create-toml parser.csv <path to schema> -n parser
   ```

   will create `parser.toml` (specified using the `-n` flag) from the
   intermediate mappings `parser.csv` file.

7. **Review TOML**: The TOML file may contain errors, so it is recommended to
   check it and alter as necessary.

8. **Run adtl**: Run adtl on the TOML file and the data source. This process
   will report validation errors, which can be fixed by reviewing the TOML file
   and looking at the source data that is invalid.

## Parser construction process (Python)

An [example notebook](example.ipynb) has been provided using the test data to demonstrate
the process of constructing a parser using the Python functions of `autoparser`.

## Troubleshooting autogenerated parsers

1. "I get validation errors like "'x' must be date":
ADTL expects dates to be provided in ISO format (i.e. YYY-MM-DD). If your dates are
formatted differently, e.g. "dd/mm/yyyy", you can add a line in the header
of the TOML file (e.g. underneath the line "returnUnmatched=True") like this:

```TOML
defaultDateFormat = "%d/%m/%Y"
```
which should automatically convert the dates for you.

2. ADTL can't find my schema (error: No such file or directory ..../x.schema.json)
AutoParser puts the path to the schema at the top of the TOML file, relative to the
*current location of the parser* (i.e, where you ran the autoparser command from).
If you have since moved the parser file, you will need to update the schema path at the
top of the TOML parser.
