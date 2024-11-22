from pathlib import Path
import autoparser
from autoparser import ParserGenerator
import pandas as pd
import tomli
import pytest
import numpy as np

ANIMAL_PARSER = ParserGenerator(
    "tests/sources/animals_mapping.csv",
    Path("tests/schemas"),
    "animals",
    config=Path("tests/test_config.toml"),
)

# TODO: sort out how lists and dicts are written out in the csv file to enable stuff to
# actually be read in properly. Maybe try and utilise some kind of schema for the
# dataframe?


def test_invalid_converter():
    with pytest.raises(NotImplementedError, match="Only ADTL is supported"):
        ParserGenerator(
            "tests/sources/animals_mapping.csv",
            Path("tests/schemas"),
            "animals",
            config=Path("tests/test_config.toml"),
            transformation_tool="invalid",
        )


def test_parsed_choices():
    parser = ANIMAL_PARSER

    choices = pd.Series(
        data=[
            None,
            None,
            None,
            None,
            None,
            {
                "mammifère": "mammal",
                "fish": "fish",
                "poisson": "fish",
                "amphibie": "amphibian",
                "oiseau": "bird",
                "autre": "",
                "rept": "reptile",
            },
            {"vivant": "alive", "décédé": "dead"},
            None,
            None,
            None,
            {"m": "male", "f": "female", "inconnu": ""},
            {"oui": True, "non": False},
            {"oui": True, "non": False},
            None,
        ],
        index=[
            "identity",
            "name",
            "loc_admin_1",
            "country_iso3",
            "notification_date",
            "classification",
            "case_status",
            "date_of_death",
            "age_years",
            "age_months",
            "sex",
            "pet",
            "chipped",
            "owner",
        ],
    )

    pd.testing.assert_series_equal(choices, parser.parsed_choices, check_names=False)


def test_references_definitions():
    parser = ANIMAL_PARSER

    ref_def = (
        {'{"non": false, "oui": true}': "Y/N/NK"},
        {"Y/N/NK": {"caseInsensitive": True, "values": {"oui": True, "non": False}}},
    )

    assert parser.references_definitions == ref_def


def test_schema_fields(snapshot):
    parser = ANIMAL_PARSER

    assert parser.schema_fields("animals") == snapshot


@pytest.mark.parametrize(
    "row, expected",
    [
        (
            pd.Series(
                data=["age_months", "Age in Months", "AgeMois", np.nan, np.nan, np.nan],
                index=[
                    "target_field",
                    "source_description",
                    "source_field",
                    "common_values",
                    "target_values",
                    "value_mapping",
                ],
            ),
            {"field": "AgeMois", "description": "Age in Months"},
        ),
        (
            pd.Series(
                data=[
                    "case_status",
                    "Case Status",
                    "StatusCas",
                    "Vivant, Décédé",
                    "alive, dead, unknown, None",
                    "vivant=alive, décédé=dead",
                ],
                index=[
                    "target_field",
                    "source_description",
                    "source_field",
                    "common_values",
                    "target_values",
                    "value_mapping",
                ],
            ),
            {
                "field": "StatusCas",
                "description": "Case Status",
                "values": {"vivant": "alive", "décédé": "dead"},
                "caseInsensitive": True,
            },
        ),
        (
            pd.Series(
                data=[
                    "pet",
                    "Pet Animal",
                    "AnimalDeCompagnie",
                    "Non, non, Oui",
                    "True, False, None",
                    "oui=True, non=False",
                ],
                index=[
                    "target_field",
                    "source_description",
                    "source_field",
                    "common_values",
                    "target_values",
                    "value_mapping",
                ],
            ),
            {
                "field": "AnimalDeCompagnie",
                "description": "Pet Animal",
                "ref": "Y/N/NK",
            },
        ),
    ],
)
def test_single_field_mapping(row, expected):
    parser = ANIMAL_PARSER

    assert parser.single_field_mapping(row) == expected


def test_create_parser(tmp_path, snapshot):
    parser = ANIMAL_PARSER

    file = tmp_path / "test.toml"

    parser.create_parser(file_name=file)

    with file.open("rb") as fp:
        parser_file = tomli.load(fp)

    # check body of parser file
    assert parser_file["animals"] == snapshot


def test_create_parser_ap_access(tmp_path, snapshot):
    file = tmp_path / "test.toml"

    autoparser.create_parser(
        "tests/sources/animals_mapping.csv",
        "tests/schemas",
        str(file),
        config="tests/test_config.toml",
    )

    with file.open("rb") as fp:
        parser_file = tomli.load(fp)

    # check body of parser file
    assert parser_file["animals"] == snapshot
