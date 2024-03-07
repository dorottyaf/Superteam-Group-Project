from .exploring_data import load_dataset, find_top_k
import pandas as pd
import pathlib

VARIABLES = ["income", "age", "educ", "ethnicity", "gender", "household", "race"]
PERIODS = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]


def top_k_change(k:int, column = "total_change", concrete = (False, "")):
    """
    Inputs:
        k: The number of top changes the function shuld give back
        column(string): The name of the column to sort by, defaults to 
        total_change
        concrete(tuple): A tuple with a boolean and a string, the boolean is
        False by default. If we only want to explore one demographiccvariable, 
        the boolean should be set to True, and the string should be the name of 
        the concrete demographic variable we want to find the top changes for

    Find the top k biggest change between any two periods of time accross all
    variables and return a sorted dictionary with the change as the key and 
    the variable and two time periods as the values.

    Returns: Sorted dictionary of the top changes with the changes as the keys
    and their respective community area, demogrpahic variable, and two time 
    periods as the value in a tuple. 
    """

    changes = {}
    variable_list = VARIABLES

    # if looking for a concrete variable, set the variable list as only that var
    if concrete[0]:
        variable_list = [concrete[1]]

    # for every variable, find the biggest changes and store them in a dictionary
    # where the value of the change is the key, and the value is a tuple containing
    # (community_area, variable, (period1, period2))
    for variable in variable_list:
        dataset = load_dataset(variable)
        for period1, period2 in PERIODS:
            k_changes = find_top_k(dataset, period1, period2, column, k)
            for __, row in k_changes.iterrows():
                changes[row[column]] = (row["community_area"], variable, \
                                        (period1, period2))

    # sort dictionary by keys in descending order to find top k biggest change
    sorted_changes = dict(sorted(changes.items(), reverse = True))

    # save the top k changes in a new dictionary
    top_k_changes = dict(list(sorted_changes.items())[0: k])
    
    return top_k_changes


def secondary_text(secondary_data:str, period1:str, period2:str, community:str):
    """
    --- Although the code looks similar for the four secondary datasources, 
    we did not have data available for every time period, and each datasource
    was unique in what time period it was missing. Due to each of them needing
    unique conditions to work, I split them into four if statements, as ageneral
    function would've been just as complicated to write with all the exceptions.
    ---
    Inputs:
        secondary_data: The name of the secondary dataset 
        period1: The first time period
        period2: The second time period
        community: The community area we want to explore

    Get the info on whether the change in the secondary data change for the 
    given time period was low, medium, or high

    Returns:A string containing information about the secondary dataset
    """

    if secondary_data == "DePaul Index":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data"\
            / "Secondary Data" / "IHS_DePaul_Index.csv"
        depaul = pd.read_csv(filename)

        # build text for DePaul
        column = period1 + " to " + period2
        change = depaul.loc[depaul["community_area"] == community, column].values[0]

        return f" and the change in the DePaul index was {change}"
    
    if secondary_data == "Evictions":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data"\
            / "Secondary Data" / "LCBH_Evictions.csv"
        evictions = pd.read_csv(filename)

        # build text for Evictions
        if period1 != "2010-2014":
            return f" and unfortunately we don't have available data on "\
                  "evictions for this time period"  
        else:
            change = evictions.loc[evictions["community_area"] == community, \
                                 "2010-2014 to 2015-2019"].values[0]
            return f" and the change in Evictions was {change}"
    
    if secondary_data == "City Permits":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data"\
            / "Secondary Data" / "City_Permit_Applications.csv"
        permits = pd.read_csv(filename)

        # build text for City Permits
        column = period1 + " to " + period2
        change = permits.loc[permits["community_area"] == community, column].values[0]

        return f" and the change in City Permits was {change}"
    
    if secondary_data == "Vacant Lot Complaints":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data"\
            / "Secondary Data" / "City_Vacant_Abandoned.csv"
        permits = pd.read_csv(filename)

        if period1 == "2005-2009":
            return f" and unfortunately we don't have available data on"\
                  "Vacant Lot Complaints for this time period"
        else:
            # build text for Vacant Lots
            column = period1 + " to " + period2
            change = permits.loc[permits["community_area"] == community, \
                                 column].values[0]

        return f" and the change in Vacant Lot Complaints was {change}"
       

def readable_change_simple(k:int, column = "total_change"):
    """
    Inputs:
        k: The number of changes to look for
        column(str): Defaults to "total_change", the name of the column to 
        sort the top k changes by

    Takes the output of top_k_change and returns a string explaining the results

    Returns: A print statement of strings explaining the result of the function
    top_k_change
    """

    # get the top changes
    top_changes = top_k_change(k, column)

    # set initial text
    text = f"The top {k} changes in Chicago were:"

    # build the rest of the strings and store them in a list
    change_info_list = []
    for key, determinants in top_changes.items():
        point = round(key * 100, 2)
        change_text = (f"In {determinants[0]} in the {determinants[1]} variable "
                        f"between {determinants[2][0]} and {determinants[2][1]}"
                        f", the change was {point} percentage points")
        change_info_list.append(change_text)
    
    # print the text
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")


def readable_change_complex(k:int, variable:str, column = "total_change", \
                            secondary = False):
    """
    Inputs:
        k: The number of top changes we're interested in
        variable: A demographic variable to find the top changes for
        column(str): Default to "total_change", the column we want to sort
        the changes by
        secondary(boolean): Defaults to False, determines whether we want to 
        print out information about a secondary dataset

    Takes the output of top_k_change when we are looking for changes in a 
    specific variable and prints out the results. Return a list of the biggest
    changes to be used by other functions.

    Returns: Various print statements explaining the result of the top_k_change
    function when we are looking for changes in a specific demographic variable,
    as well as returns a list of the top changes where each entry in the list is 
    a tuple containing (index, community are, period1, period2).
    """

    # get top changes for a given variable
    concrete = (True, variable)
    top_changes = top_k_change(k, column, concrete)

    # build initial text
    if column == "total_change":
        text = f"The top {k} changes for the {variable} variable were:"
    else:
        text = (f"The top {k} changes in the {column} category" 
                f"for the {variable} variable were:")
    
    # build rest of text
    change_info_list = []
    indexed_list = []
    i = 0

    for key, determinants in top_changes.items():
        i += 1
        point = round(key * 100, 2)
        change_text = (f"In {determinants[0]} between {determinants[2][0]} " 
                       f"and {determinants[2][1]}"
                       f", the change was {point} percentage points")
        indexed_list.append((i, determinants[0], determinants[2][0], \
                             determinants[2][1]))
        # if user wants information from a secondary data source, 
        # add it to the end of sentence
        if secondary:
            change_text = change_text + secondary_text(secondary, \
                                                        determinants[2][0], \
                                                        determinants[2][1], \
                                                        determinants[0])
        change_info_list.append(change_text)
    
    # print the readable text
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")
    
    # return list so the information can be stored
    return indexed_list
