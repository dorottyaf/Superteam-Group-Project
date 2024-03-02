from exploring_data import load_dataset, find_top_k
import pandas as pd
import pathlib

VARIABLES = ["income", "age", "educ", "ethnicity", "gender", "household", "race"]
PERIODS = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]


def biggest_change(dataset:str, period1: str, period2:str, num_results:int, column):
    """
    This is almost identical to the explore function in demonstration.py
    with the change that the output is a pandas dataframe. I just wanted to 
    preserve the explore function for internal interpretations, so I recreated 
    it here
    """
    data = load_dataset(dataset)
    top_changes = find_top_k(data, period1, period2, column, num_results)
    
    return top_changes


def top_k_change(k, column = "total_change", concrete = (False, "")):
    """
    Find the top k biggest change between any two periods of time accross all
    variables and return a sorted dictionary with the change as the key and 
    the variable and two periods as the values
    """

    changes = {}
    variable_list = VARIABLES

    if concrete[0]:
        variable_list = [concrete[1]]

    for variable in variable_list:
        for period1, period2 in PERIODS:
            k_changes = biggest_change(variable, period1, period2, k, column)
            for __, row in k_changes.iterrows():
                changes[row[column]] = (row["community_area"], variable, (period1, period2))

    # sort dictionary by keys in descending order
    sorted_changes = dict(sorted(changes.items(), reverse = True))

    # save the top k changes in a new dictionary
    top_k_changes = dict(list(sorted_changes.items())[0: k])
    
    return top_k_changes


def secondary_text(secondary_data:str, period1:str, period2:str, community:str):
    """
    Get the info on whether the secondary data change in the time period was
    low, medium, or high
    """

    if secondary_data == "depaul":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
        depaul = pd.read_csv(filename)

        column = period1 + " to " + period2
        change = depaul.loc[depaul["community_area"] == community, column].values[0]

        return f"and the change in the DePaul index was {change}"
        


def readable_change_simple(k, column = "total_change", secondary = False):
    """
    Takes the output of top_k_change and returns a string explaining the results
    """

    top_changes = top_k_change(k, column)
    text = f"The top {k} changes in Chicago were:"

    change_info_list = []
    for __, determinants in top_changes.items():
        change_text = f"In {determinants[0]} in the {determinants[1]} variable between {determinants[2][0]} and {determinants[2][1]}"
        if secondary:
            change_text = change_text + secondary_text(secondary,determinants[2][0], determinants[2][1], determinants[0])
        change_info_list.append(change_text)
    
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")


def readable_change_complex(k, variable, column = "total_change", secondary = False):
    """
    Takes the output of top_k_change when we are looking for changes in a 
    specific variable and prints out the results
    """

    concrete = (True, variable)
    top_changes = top_k_change(k, column, concrete)

    if column == "total_change":
        text = f"The top {k} changes for the {variable} variable were:"
    else:
        text = f"The top {k} changes in the {column} category for the {variable} variable were:"
    
    change_info_list = []
    for __, determinants in top_changes.items():
        change_text = f"In {determinants[0]} between {determinants[2][0]} and {determinants[2][1]}"
        change_info_list.append(change_text)
    
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")


readable_change_simple(10, secondary="depaul")
# readable_change_complex(10, "household")
