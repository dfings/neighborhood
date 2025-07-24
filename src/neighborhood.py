"""
Library that takes a data file produced by join_data.py and an address
(street number, name, and type) and produces the SF neighborhood that
address is in.

The joined data file is tab-separated with the following fields:
StreetName	StreetType	SideCode	HouseNumLo	HouseNumHi	Neighborhood

A given address is matches a row if the StreetName and StreetType match,
and the street number is in the range defined by SideCode, HouseNumLo, and
HouseNumHi.
"""

from dataclasses import dataclass
import os
import string
from typing import Final, List

import polars as pl
import scourgify
import usaddress


_DATA: Final = pl.read_csv(
    os.path.join(os.path.dirname(__file__), "data/neighborhood_data.tsv"),
    separator="\t",
)


@dataclass(frozen=True)
class StreetAddress:
    number: int
    name: str
    type: str

    @property
    def side_code(self) -> str:
        return "O" if self.number % 2 else "E"


def parse_street_address(street_address: str) -> StreetAddress:
    """Parses a raw street address to (number, name, type)."""
    if not street_address:
        raise ValueError("Empty address")
    try:
        normalized = scourgify.normalize_address_record(street_address)
    except scourgify.exceptions.UnParseableAddressError as ex:
        raise ValueError(ex) from ex
    parsed, _ = usaddress.tag(normalized["address_line_1"])
    street_number: str = parsed.get("AddressNumber")
    if not street_number:
        raise ValueError(str(parsed))
    return StreetAddress(
        int(street_number.rstrip(string.ascii_letters)),
        parsed.get("StreetName", "").lower(),
        parsed.get("StreetNamePostType", "").lower(),
    )


@dataclass(frozen=True, order=True)
class Result:
    district: int
    neighborhood: str


def find(raw_street_address: str) -> List[Result]:
    """
    Given the loaded data and the input address, finds rows that match.
    If the street_type doesn't exist for a given street, we'll fall back
    to all street types for that street.
    """
    try:
        street_address = parse_street_address(raw_street_address)
    except ValueError:
        return []
    name_restrict = pl.col("StreetName") == street_address.name
    type_restrict = pl.col("StreetType") == street_address.type
    street_data = _DATA.filter(name_restrict & type_restrict)
    if street_data.is_empty():
        street_data = _DATA.filter(name_restrict)
    matches = street_data.filter(
        (pl.col("SideCode").is_in([street_address.side_code, "A"]))
        & (pl.col("HouseNumLo") <= street_address.number)
        & (pl.col("HouseNumHi") >= street_address.number)
    )
    return sorted(
        {Result(row["District"], row["Neighborhood"]) for row in matches.to_dicts()}
    )
