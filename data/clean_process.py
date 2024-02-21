import pathlib
from conversion_dics import age_conversion, educ_conversion, income_conversion
from column_conversion import age_dictionary, educ_dictionary, income_dictionary, \
    ethnicity_dictionary, gender_dictionary, household_dictionary, race_dictionary
from combination_dicts import age_categories, income_categories, household_categories

import pandas as pd


# list of years and variables
years = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]
# dictionary of the datasets for a variable, and their conversion dictionary
# in a tuple
variables = {
    "age": ([], age_dictionary, age_categories),
    "ethnicity": ([], ethnicity_dictionary),
    "household": ([], household_dictionary, household_categories),
    "educ": ([], educ_dictionary),
    "gender": ([], gender_dictionary),
    "income": ([], income_dictionary, income_categories),
    "race": ([], race_dictionary),
}
     
        
def get_one_dataset(period:str, variable_name: str, variable_tuple: tuple):
    """
    Load in the raw data, append some missing columns, and append it to the list
    in its corresponding dictionary
    """
    current_file = variable_name + "_" + period + ".csv"
    filename = pathlib.Path(__file__).parent / "raw_data" / period / current_file
    data = pd.read_csv(filename)

    # fixing 2005-2009 data
    if period == "2005-2009":
        data = fix_2005_2009_data(data, variable_name)

    # loading the population data to add to the dataframe
    population_file = "population_" + period + ".csv"
    popfile = pathlib.Path(__file__).parent / "raw_data" / period / population_file
    pop_data = pd.read_csv(popfile)
    
    # creating a variable to record the population
    if period == "2005-2009" or period == "2010-2014":
        data["population"] = pop_data["B01001_001E"]
    if period == "2015-2019" or period == "2018-2022":
        data["population"] = pop_data["B01003_001E"]

    # creating a variable to record the period
    data["period"] = [period] * len(data)
        
    # adding data to the dictionary
    variable_tuple[0].append(data)

    return variable_tuple


def fix_2005_2009_data(data: pd, variable_name: str):
    """
    Fixes the age, education, and income variable in a pandas dataframe
    
    Returns the fixed dataframe
    """
    if variable_name == "age":
            for new, old in age_conversion.items():
                data = combine_columns(new, old, data)
            
    if variable_name == "educ":
        for new, old in educ_conversion.items():
            data = combine_columns(new, old, data)

    if variable_name == "income":
        for new, old in income_conversion.items():
            if new == "B06010_002E":
                name_column_index = data.columns.get_loc("NAME")
                data.insert(name_column_index + 1, new, pd.NA)
                continue
            data = combine_columns(new, old, data)
    
    return data


def make_combined_datasets(variable_name: str, variable_tuple: tuple):
    """
    Combine the different datasets for a variable into one large dataset
    """
    #combine datasets into one large one and rename them
    data = pd.concat(variable_tuple[0])
    data.rename(columns = variable_tuple[1], inplace = True)

    # combine some columns in age, income, household income
    data = combine_age_income_household(data, variable_name, variable_tuple)

    # save the clean dataset
    name = variable_name + "_data.csv"
    filename = pathlib.Path(__file__).parent / "clean_data" / name
    data.to_csv(filename)


def combine_columns(new_name: str, old_names: list, dataframe: pd):
    """
    Combines columns in a dataframe into a new column
    """
    dataframe.rename(columns = {old_names[0] : new_name}, inplace = True)
    for instance in old_names[1:]:
        dataframe[new_name] = dataframe[new_name] + dataframe[instance]
        dataframe = dataframe.drop(instance, axis = "columns")
    
    return dataframe


def combine_age_income_household(dataframe: pd, variable_name: str, variable_tuple: tuple):
    """
    Rearrange the data in the age, income, and household columns into fewer
    "buckets" to help wiht analysis
    """

    if variable_name == "age":
        for new, old in variable_tuple[2].items():
            dataframe = combine_columns(new, old, dataframe)
    
    if variable_name == "income":
        for new, old in variable_tuple[2].items():
            dataframe = combine_columns(new, old, dataframe)
    
    if variable_name == "household":
        for new, old in variable_tuple[2].items():
            dataframe = combine_columns(new, old, dataframe)
    
    return dataframe


for name, tuples in variables.items():
    for period in years:
        tuples = get_one_dataset(period, name, tuples)
    make_combined_datasets(name, tuples)
