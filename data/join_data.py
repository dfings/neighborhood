#! /usr/bin/env python

"""
Utility for taking SF's public "Street Data Extract" data set
(https://sfelections.org/tools/election_data/dataset.php?ATAB=d1970-01-01)
and the proprietary precincts.tsv file which maps precinct number to district
and neighborhood, producing a data set that can be used by find_neighborhood.py
to determine neighborhood given a street address.

Sample usage:
  ./join_data.py elections-data.txt precincts.tsv > ../src/data/neighborhood_data.tsv
"""

import sys

import polars as pl

OUTPUT_COLUMNS = [
    "StreetName",
    "StreetType",
    "SideCode",
    "HouseNumLo",
    "HouseNumHi",
    "District",
    "Neighborhood",
]


def join_election_data(election_filename: str, precinct_filename: str) -> None:
    """Joins the two datasets and outputs to stdout."""
    election_data = pl.read_csv(election_filename, separator="\t")
    precinct_data = pl.read_csv(precinct_filename, separator="\t")
    assert precinct_data["PrecinctID"].is_unique().all()
    data = election_data.join(precinct_data, on="PrecinctID", how="inner")
    # Filter out weird records
    data = data.filter(~pl.col("StreetName").str.starts_with("@"))
    data = data.with_columns(
        pl.col("StreetName").str.to_lowercase(),
        pl.col("StreetType").str.to_lowercase(),
        pl.col("SideCode").str.to_uppercase(),
    )
    data = data.sort(by=OUTPUT_COLUMNS)
    data.select(OUTPUT_COLUMNS).write_csv(sys.stdout, separator='\t')



if __name__ == "__main__":
    assert len(sys.argv) == 3
    join_election_data(sys.argv[1], sys.argv[2])
