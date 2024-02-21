import pandas as pd
import pathlib

EXCEPTION = ["NAME", "state", "county", "tract", "population", "period"]

def load_dataset(variable_name:str):
    dataset = variable_name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / dataset
    data = pd.read_csv(filename)

    return data

def difference_between_years(dataframe:pd, period1:str, period2:str):
    """
    Given a dataframe and two periods of time, the function calculates the 
    difference in values between the two years
    """

    # subtract the two years we're interested in
    df_period1 = dataframe[dataframe["period"] == period1]
    df_period2 = dataframe[dataframe["period"] == period2]

    # merge on track
    merged_df = pd.merge(df_period1, df_period2, on = "tract", suffixes=("_period1", "_period2"))

    differences_df = pd.DataFrame()

    # iterate through columns if they are not constants
    for col in dataframe.columns.difference(EXCEPTION):
        # Create a new column for differences
        differences_df[col] = merged_df[col + "_period1"] - merged_df[col + "_period2"]
    
    absolute = differences_df.abs()
    
    # put in a total_change column and put back the tracts
    differences_df["total_change"] = absolute.sum(axis=1)
    differences_df["tract"] = merged_df["tract"]

    return differences_df

def find_top_k(dataframe: pd, period1: str, period2: str, variable: str, k:int):

    differences = difference_between_years(dataframe, period1, period2)

    # sort by descending order
    differences = differences.sort_values(by=[variable], ascending=False)

    # get the first k entries
    sorted_k_data = differences.head(k)
    return sorted_k_data

def detailed_top_k(dataframe:str, period1: str, period2: str, variable: str,):
    """
    Print out more information about the changes in a tract between two years
    """

    # put the top_k tracts in a list
    tract_list = dataframe["tract"].tolist()

    # reload old dataframe and save its columns
    og_dataframe = load_dataset(variable)
    column_list = og_dataframe.columns.difference(EXCEPTION).tolist()

    strings = []

    # make the helper string
    for tract in tract_list:
        text = "In tract " + str(tract)
        for column in column_list:
            og_value = round(og_dataframe.loc[(og_dataframe["period"] == period1) & (og_dataframe["tract"] == tract), column].iloc[0], 3)
            new_value = round(og_dataframe.loc[(og_dataframe["period"] == period2) & (og_dataframe["tract"] == tract), column].iloc[0], 3)
            text += f", {column} changed from {og_value} to {new_value}"
    
        strings.append(text)

    return strings

