"Contains all functions that call Google's Gemini API."
import google.generativeai as gemini
from .util import ColumnDescriptionRequest, MappingRequest, ValuesRequest


def _get_definitions(
    headers: list[str], language: str, client: gemini
) -> dict[str, str]:
    """
    Get the definitions of the columns in the dataset.
    """
    model = client.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [
            (
                "You are an expert at structured data extraction. "
                "The following is a list of headers from a data file in "
                f"{language}, some containing shortened words or abbreviations. "
                "Translate them to english. "
                "Return a list of (original header, translation) pairs, using the given structure."  # noqa
            ),
            f"{headers}",
        ],
        generation_config=client.GenerationConfig(
            response_mime_type="application/json",
            response_schema=ColumnDescriptionRequest,
        ),
    )
    descriptions = result.field_descriptions
    return descriptions


def _map_fields(
    source_fields: list[str], target_fields: list[str], client: gemini
) -> MappingRequest:
    """
    Calls the Gemini API to generate a draft mapping between two datasets.
    """
    model = client.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [
            (
                "You are an expert at structured data extraction. "
                "You will be given two lists of phrases, one is the headers for a "
                "target data file, and the other a set of descriptions for columns "
                "of source data. "
                "Match each target header to the best matching source description, "
                "but match a header to None if a good match does not exist. "
                "Return the matched target headers and source descriptions using the provided structure."  # noqa
            ),
            (
                f"These are the target headers: {target_fields}\n"
                f"These are the source descriptions: {source_fields}"
            ),
        ],
        generation_config=client.GenerationConfig(
            response_mime_type="application/json",
            response_schema=MappingRequest,
        ),
    )
    return result


def _map_values(
    values: list[tuple[set[str], set[str], list[str]]], language: str, client: gemini
) -> ValuesRequest:
    """
    Calls the Gemini API to generate a set of value mappings for the fields.
    """
    model = client.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [
            (
                "You are an expert at structured data extraction. "
                "You will be given a list of tuples, where each tuple contains "
                "three sets of string values. "
                "The first set contains field names for a dataset."
                "The second set contains values from a source dataset in "
                f"{language}, and the third set contains target values for an "
                "english-language transformed dataset. "
                "Match all the values in the second set to the appropriate values "
                "in the third set. "
                "Return a list of dictionaries, where each dictionary contains the "
                "field name as a key, and a dictionary containing "
                "source values as keys, and the target text as values, "
                "as the values. For example, the result should look like this: "
                "[{'field_name_1': {'source_value_a': 'target_value_a', "
                "'source_value_b': 'target_value_b'}, 'field_name_2':{...}]"
                "using the provided structure."
            ),
            f"These are the field, source, target value sets: {values}",
        ],
        generation_config=client.GenerationConfig(
            response_mime_type="application/json",
            response_schema=ValuesRequest,
        ),
    )
    return result
