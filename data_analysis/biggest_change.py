from exploring_data import load_dataset, find_top_k
import pandas as pd

variables = ["income", "age", "educ", "ethnicity", "gender", "household", "race"]
periods = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]


def biggest_change(dataset:str, period1: str, period2:str, num_results:int, column):
    """
    This is almost identical to the explore function in demonstration.py
    with the change the output is a pandas dataframe. I just wanted to preserve
    the explore function for internal interpretations, so I recreated it here
    """
    data = load_dataset(dataset)
    top_changes = find_top_k(data, period1, period2, column, num_results)
    
    return top_changes


def top_k_change(k, column = "total_change"):
    """
    Find the top k biggest change between any two periods of time accross all
    variables and return a sorted dictionary with the change as the key and 
    the variable and two periods as the values
    """

    changes = {}

    for variable in variables:
        for period1, period2 in periods:
            k_changes = biggest_change(variable, period1, period2, k, column)
            for index, row in k_changes.iterrows():
                changes[row[column]] = (row["community_area"], variable, (period1, period2))

    # sort dictionary by keys in descending order
    sorted_changes = dict(sorted(changes.items(), reverse = True))

    # save the top k changes in a new dictionary
    top_k_changes = dict(list(sorted_changes.items())[0: k])
    
    return top_k_changes


def readeable_change(k, column = "total_change"):
    """
    Takes the output of top_k_change and returns a string explaining the results
    """

    top_changes = top_k_change(k, column)
    text = f"The top {k} changes in Chicago were:"

    change_info_list = []
    for change, determinants in top_changes.items():
        change_text = f"In {determinants[0]} in the {determinants[1]} variable between {determinants[2][0]} and {determinants[2][1]}"
        change_info_list.append(change_text)
    
    print(text)
    for index, message in enumerate(change_info_list):
        print (f"{index + 1} {message}")



readeable_change(4)
