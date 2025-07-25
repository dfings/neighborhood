import pytest

import neighborhood
from neighborhood import Result


def assert_parse(
    street_address: str, street_number: int, street_name: str, street_type: str
) -> None:
    expected = neighborhood.StreetAddress(
        number=street_number,
        name=street_name,
        type=street_type,
    )
    assert neighborhood.parse_street_address(street_address) == expected


def test_basic_parse() -> None:
    assert_parse("123 Main St", 123, "main", "st")


def test_apt_number_parse() -> None:
    assert_parse("123 Main St #101", 123, "main", "st")


def test_street_type_normalization() -> None:
    assert_parse("123 Main Street", 123, "main", "st")


def test_apt_number_parse_with_suite() -> None:
    assert_parse("123 Main St Suite 101", 123, "main", "st")


def test_street_type_missing() -> None:
    assert_parse("123 Main", 123, "main", "")


def test_number_with_letter_suffix() -> None:
    assert_parse("123b Main St", 123, "main", "st")
    assert_parse("123 Main St b", 123, "main", "st")


def test_number_value_error() -> None:
    with pytest.raises(ValueError):
        neighborhood.parse_street_address("b123 Main St")


def test_empty_error() -> None:
    with pytest.raises(ValueError):
        neighborhood.parse_street_address("")


def assert_find_results(street_address: str, *results: Result) -> None:
    assert neighborhood.find(street_address) == list(results)


def test_street_match() -> None:
    assert_find_results(
        "123 Main St", Result(district=6, neighborhood="Financial District/South Beach")
    )


def test_padded_street_match() -> None:
    assert_find_results(
        "   123 Main St   ",
        Result(district=6, neighborhood="Financial District/South Beach"),
    )


def test_full_address() -> None:
    assert_find_results(
        "123 Main St, San Francisco, CA 94105",
        Result(district=6, neighborhood="Financial District/South Beach"),
    )


def test_street_type_missing_find() -> None:
    assert_find_results(
        "123 Main", Result(district=6, neighborhood="Financial District/South Beach")
    )


def test_junk_suffix() -> None:
    assert_find_results(
        "123 Main Suite 100",
        Result(district=6, neighborhood="Financial District/South Beach"),
    )


def test_random_suffix() -> None:
    assert_find_results(
        "123 Main Suite 100",
        Result(district=6, neighborhood="Financial District/South Beach"),
    )


def test_unparseable_address() -> None:
    assert_find_results("1 10th")
    assert_find_results("1 10th Apt 3")
    assert_find_results("b123 Main St")


def test_no_match() -> None:
    assert_find_results("1 asdf123 st")


def test_empty_input() -> None:
    assert_find_results(" ")
    assert_find_results("")
