# tests the `DictWriter` class
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


def test_dictionary_creation_no_descrip():
    writer = DictWriter(config=Path("tests/test_config.toml"))

    df = writer.create_dict("tests/sources/animal_data.csv")

    df_desired = pd.read_csv("tests/sources/animals_dd.csv")

    pd.testing.assert_frame_equal(df, df_desired)


def test_dictionary_description():
    writer = DictWriterTest(config=Path("tests/test_config.toml"))

    df = writer.generate_descriptions("fr", "tests/sources/animals_dd.csv")

    df_desired = pd.read_csv("tests/sources/animals_dd_described.csv")

    pd.testing.assert_frame_equal(df, df_desired)


def test_wrong_llm_error():
    with pytest.raises(ValueError, match="Unsupported LLM: fish"):
        DictWriter(config=Path("tests/test_config.toml")).generate_descriptions(
            "fr", "tests/sources/animals_dd.csv", llm="fish"
        )
