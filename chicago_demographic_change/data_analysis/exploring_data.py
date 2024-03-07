import pandas as pd
import pathlib

EXCEPTION = ["NAME", "state", "county", "community_area", "population", "period"]


def load_dataset(variable_name:str):
    dataset = variable_name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / dataset
    data = pd.read_csv(filename)

    return data


def difference_between_years(dataframe:pd, period1:str, period2:str):
    """
    Inputs:
        dataframe: A Pandas Dataframe with the proportions of certain 
        demographic variables organised by community areas
        period1: the first period of time
        period2: the second period of time 

    Given a dataframe and two periods of time, the function calculates the 
    difference in values between the two years

    Returns: 
        A Pandas Dataframe where the values are the differences in proportion
        between the given time periods. The function also creates a "total_change"
        column which captures the total absolute change between the time periods
    """

    # subtract the two years we're interested in
    df_period1 = dataframe[dataframe["period"] == period1]
    df_period2 = dataframe[dataframe["period"] == period2]

    # merge on track
    merged_df = pd.merge(df_period1, df_period2, on = "community_area", suffixes=("_period1", "_period2"))

    differences_df = pd.DataFrame()

    # iterate through columns if they are not constants
    for col in dataframe.columns.difference(EXCEPTION):
        # Create a new column for differences
        differences_df[col] = merged_df[col + "_period2"] - merged_df[col + "_period1"]
    
    absolute = differences_df.abs()
    
    # put in a total_change column and put back the tracts
    differences_df["total_change"] = absolute.sum(axis=1)
    differences_df["community_area"] = merged_df["community_area"]

    return differences_df


def find_top_k(dataframe: pd, period1: str, period2: str, column: str, k:int):
    """
    Inputs:
        dataframe: A Pandas Dataframe with the proportions of certain 
        demographic variables organised by community areas
        period1: the first period of time
        period2: the second period of time
        column: the column of the dataframe to sort by when finding the 
        biggest changes
        k: the number of results to get back

    Finds the top k changes in a community area between the given time periods
    by calculating the difference between the two time periods, and sorting
    based on the given column.

    Returns: A sorted dataframe
    """

    differences = difference_between_years(dataframe, period1, period2)

    # sort by descending order
    differences = differences.sort_values(by=[column], ascending=False)

    # get the first k entries
    sorted_k_data = differences.head(k)

    return sorted_k_data


def detailed_top_k(dataframe:str, period1: str, period2: str, variable: str,):
    """
    --- Our app does not end up using this function, we used it internally
    to explore the data in the beginning ---

    Inputs:
        dataframe: A Pandas Dataframe with the proportions of certain 
        demographic variables organised by community areas
        period1: the first period of time
        period2: the second period of time
        vairable: a demographic variable we want to find the top changes for

    Prints out more information about the changes in a Community Area between 
    two periods. Taking the two periods, the function looks column by column
    to calculate the changes in values, and prints out a detailed list of changes
    for each community area.

    Returns: A list of strings containing information about the changes
    """

    # put the top_k Community Areas in a list
    comm_area_list = dataframe["community_area"].tolist()

    # reload old dataframe and save its columns
    og_dataframe = load_dataset(variable)
    column_list = og_dataframe.columns.difference(EXCEPTION).tolist()

    strings = []

    # make the helper string
    for comm_area in comm_area_list:
        text = "In Community Area " + str(comm_area)
        for column in column_list:
            og_value = round(og_dataframe.loc[(og_dataframe["period"] == period1)\
                             & (og_dataframe["community_area"] == comm_area), column].iloc[0], 3)
            new_value = round(og_dataframe.loc[(og_dataframe["period"] == period2) \
                            & (og_dataframe["community_area"] == comm_area), column].iloc[0], 3)
            text += f", {column} changed from {og_value} to {new_value}"
    
        strings.append(text)

    return strings
