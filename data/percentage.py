import pandas as pd
import pathlib
from .cleaning import variables

EXCLUDE = ["NAME", "state", "county", "tract", "population", "period"]

def load_in_dataframe(name:str):
    csv_name = name + "_data.csv"
    filename = pathlib.Path(__file__).parent / "clean_data" / csv_name
    data = pd.read_csv(filename, index_col=0)

    return data

def create_percentage_data(dataframe: pd):
    """
    Create a secondary set of datasets which shows what the proportion is of
    a given obseration compared to the percentage of the tract
    """

    for column in dataframe.columns:
        if column not in EXCLUDE:
            dataframe = calculate_percentage(dataframe, column)
    
    return dataframe

def calculate_percentage(dataframe: pd, column_name: str):
    """
    Calculates the proportions for one column
    """

    dataframe[column_name] = dataframe[column_name] / dataframe["population"]

    return dataframe

def make_percentage_files():
    """
    Create the percentage files based on the clean datasets
    """

    for variable in variables:
        data = load_in_dataframe(variable)
        data = create_percentage_data(data)

        name = variable + "_percentage_data.csv"
        filename = pathlib.Path(__file__).parent / "clean_data" / name
        data.to_csv(filename)

make_percentage_files()