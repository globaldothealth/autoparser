# tests the `DictWriter` class
import autoparser
from autoparser.dict_writer import DictWriter
from pathlib import Path

from testing_data_animals import get_definitions
import pandas as pd
import pytest


class DictWriterTest(DictWriter):
    def __init__(
        self,
        config: Path | None = None,
    ):
        super().__init__(config)

    def _setup_llm(self, key, name):
        self.client = None
        self._get_descriptions = get_definitions


def test_unsupported_data_format_txt():
    writer = DictWriter(config="tests/test_config.toml")

    with pytest.raises(ValueError, match="Unsupported format"):
        writer.create_dict("tests/sources/animals.txt")


def test_data_not_df_or_path():
    writer = DictWriter(config="tests/test_config.toml")

    with pytest.raises(ValueError, match="Data must be a path"):
        writer.create_dict(None)


def test_dictionary_creation_no_descrip():
    writer = DictWriter(config="tests/test_config.toml")

    df = writer.create_dict("tests/sources/animal_data.csv")

    df_desired = pd.read_csv("tests/sources/animals_dd.csv")

    pd.testing.assert_frame_equal(df, df_desired)


def test_create_dict_no_descrip():
    df = autoparser.create_dict(
        "tests/sources/animal_data.csv", config="tests/test_config.toml"
    )

    df_desired = pd.read_csv("tests/sources/animals_dd.csv")

    pd.testing.assert_frame_equal(df, df_desired)


def test_dictionary_creation_no_descrip_excel_dataframe():
    writer = DictWriter(config="tests/test_config.toml")

    # check no errors excel
    writer.create_dict("tests/sources/animal_data.xlsx")

    # check no errors dataframe
    df = pd.read_csv("tests/sources/animals_dd.csv")
    writer.create_dict(df)


def test_dictionary_description():
    writer = DictWriterTest(config=Path("tests/test_config.toml"))

    # check descriptions aren't generated without a dictionary
    with pytest.raises(ValueError, match="No data dictionary found"):
        writer.generate_descriptions("fr")

    df = writer.generate_descriptions("fr", "tests/sources/animals_dd.csv")

    df_desired = pd.read_csv("tests/sources/animals_dd_described.csv")

    pd.testing.assert_frame_equal(df, df_desired)


def test_missing_key_error():
    with pytest.raises(ValueError, match="API key required"):
        DictWriter(config=Path("tests/test_config.toml")).generate_descriptions(
            "fr", "tests/sources/animals_dd.csv"
        )


def test_wrong_llm_error():
    with pytest.raises(ValueError, match="Unsupported LLM: fish"):
        DictWriter(config=Path("tests/test_config.toml")).generate_descriptions(
            "fr", "tests/sources/animals_dd.csv", key="a12b3c", llm="fish"
        )
