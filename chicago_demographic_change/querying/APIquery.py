from census import Census
import pandas as pd
import os

key = os.environ["census_API_key"]


def make_pull(input_year, col_names, filename):
    """
    Pulling a group of census variables for all tracts in Cook County, IL
    for a specific year

    Args:
        year(int): year we're pulling
        col_names(tuple): tuple of the fields we're pulling
        filename(str): desired name of output file (must end in .csv)
    """

    c = Census(key)

    census = c.acs5.state_county_tract(
        fields=col_names, state_fips="17", county_fips="031", tract="*", year=input_year
    )

    census_df = pd.DataFrame(census)
    census_df.to_csv(filename, index=False)


# NOTE: Different function due to changes in the census package's convenience
# methods and changes in census geography for 2022
def make_pull_2022(col_names, filename):
    """
    Pulling a group of census variables for all tracts in Cook County, IL
    for the year 2022 specifically

    Args:
        col_names(tuple): tuple of the fields we're pulling
        filename(str): desired name of output file (must end in .csv)
    """
    c = Census(key, year=2022)
    census = c.acs5.get(col_names, {"for": "tract:*", "in": "state:17 county:031"})
    census_df = pd.DataFrame(census)
    census_df.to_csv(filename, index=False)
