# read_data
# parse_choices
# load_data_dict

import pytest
from pathlib import Path
import numpy.testing as npt
import pandas as pd

from autoparser.util import read_data, parse_choices, load_data_dict

CONFIG = read_data(Path("tests/test_config.toml"))


def test_read_data():
    data = read_data(Path("tests/test_config.toml"))
    assert isinstance(data, dict)
    npt.assert_array_equal(
        [
            "name",
            "description",
            "choice_delimiter",
            "choice_delimiter_map",
            "num_refs",
            "num_choices",
            "schemas",
            "column_mappings",
        ],
        list(data.keys()),
    )

    data = read_data(Path("tests/schemas/animals.schema.json"))
    assert isinstance(data, dict)
    npt.assert_array_equal(
        ["$schema", "$id", "title", "description", "required", "properties"],
        list(data.keys()),
    )

    with pytest.raises(ValueError, match="Unsupported file format: .csv"):
        read_data(Path("tests/sources/animals_dd_described.csv"))


@pytest.mark.parametrize(
    "s, expected",
    [
        ("oui=True, non=False, blah=None", {"oui": True, "non": False, "blah": ""}),
        ("vivant=alive, décédé=dead, " "=None", {"vivant": "alive", "décédé": "dead"}),
        ({2: True}, None),
        ("" " = " ", poisson=fish", {"poisson": "fish"}),
    ],
)
def test_parse_choices(s, expected):
    choices = parse_choices(CONFIG, s)
    assert choices == expected


def test_parse_choices_error():
    # dictionary printed without stringification
    with pytest.raises(ValueError, match="Invalid choices list"):
        parse_choices(CONFIG, '{"oui":"True", "non":"False", "blah":"None"}')

    # different choice_delimeter_map
    with pytest.raises(ValueError, match="Invalid choices list"):
        parse_choices(CONFIG, "oui:True, non:False, blah:None")


def test_load_data_dict():
    dd_original = pd.read_csv("tests/sources/animals_dd.csv")

    npt.assert_array_equal(
        list(dd_original.columns),
        [
            "Field Name",
            "Description",
            "Field Type",
            "Common Values",
        ],
    )

    data = load_data_dict(CONFIG, "tests/sources/animals_dd.csv")
    npt.assert_array_equal(
        data.columns,
        ["source_field", "source_description", "source_type", "common_values"],
    )

    with pytest.raises(ValueError, match="Unsupported format"):
        load_data_dict(CONFIG, "tests/sources/animals.txt")
