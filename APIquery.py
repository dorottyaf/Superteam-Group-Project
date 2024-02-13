from census import Census
import pandas as pd


def make_pull(input_year, col_names, filename):
    """
    Pulling the category of interest for the year of interest

    Args:
        year(int): year we're pulling
        col_names(tuple): tuple of the fields we're pulling
        filename(str): desired name of output file (must end in .csv)
    """

    c = Census("0755e3aa241f128b77440898d8df6d9cc5109d4f")
    
    census = c.acs5.state_county_tract(fields = col_names,
                                        state_fips = "17",
                                        county_fips = "031",
                                        tract = "*",
                                        year=input_year)
    
    census_df = pd.DataFrame(census)
    census_df.to_csv(filename, index=False)


def make_pull_2022(col_names, filename):
    """
    Pulling the category of interest for the 2022 ACS 5-Year Dataset

    Args:
        col_names(tuple): tuple of the fields we're pulling
        filename(str): desired name of output file (must end in .csv)
    """
    c = Census("0755e3aa241f128b77440898d8df6d9cc5109d4f", year=2022)
    census = c.acs5.get(col_names, {'for': 'tract:*', 'in': 'state:17 county:031'})
    census_df = pd.DataFrame(census)
    census_df.to_csv(filename, index=False)