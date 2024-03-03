from exploring_data import load_dataset, find_top_k
import pandas as pd
import pathlib

VARIABLES = ["income", "age", "educ", "ethnicity", "gender", "household", "race"]
PERIODS = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]


def top_k_change(k, column = "total_change", concrete = (False, "")):
    """
    Find the top k biggest change between any two periods of time accross all
    variables and return a sorted dictionary with the change as the key and 
    the variable and two periods as the values
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
    Get the info on whether the secondary data change in the time period was
    low, medium, or high
    """

    if secondary_data == "DePaul_Index":
        # load data
        filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data"\
            / "Secondary Data" / "IHS_DePaul_Index.csv"
        depaul = pd.read_csv(filename)

        # build text for DePaul
        column = period1 + " to " + period2
        change = depaul.loc[depaul["community_area"] == community, column].values[0]

        return f" and the change in the DePaul index was {change}"
        

def readable_change_simple(k, column = "total_change"):
    """
    Takes the output of top_k_change and returns a string explaining the results
    """

    # get the top changes
    top_changes = top_k_change(k, column)

    # set initial text
    text = f"The top {k} changes in Chicago were:"

    # build the rest of the strings and store them in a list
    change_info_list = []
    for key, determinants in top_changes.items():
        point = round(key, 2)
        change_text = (f"In {determinants[0]} in the {determinants[1]} variable "
                        f"between {determinants[2][0]} and {determinants[2][1]}"
                        f", the change was {point} percentage points")
        change_info_list.append(change_text)
    
    # print the text
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")


def readable_change_complex(k, variable, column = "total_change", \
                            secondary = False):
    """
    Takes the output of top_k_change when we are looking for changes in a 
    specific variable and prints out the results
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
        point = round(key, 2)
        change_text = (f"In {determinants[0]} between {determinants[2][0]} " 
                       f"and {determinants[2][1]}"
                       f", the change was {point} percentage points")
        indexed_list.append((i, determinants[0], determinants[2][0], determinants[2][1]))
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
