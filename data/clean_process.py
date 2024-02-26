import pathlib
from .tract_matching import get_community_areas
from .conversion_dics import age_conversion, educ_conversion, income_conversion
import pandas as pd
    
        
def get_one_dataset(period:str, variable_name: str, variable_tuple: tuple):
    """
    For one variable in one time period, get the raw data, add a population column,
    add a column to record the time period, and convert the tracts to community
    areas.

    Essentially get one complete dataset for a given variable at a given timeperiod,
    then append it to it's corresponding variable list
    """
    current_file = variable_name + "_" + period + ".csv"
    filename = pathlib.Path(__file__).parent / "raw_data" / period / current_file
    data = pd.read_csv(filename)

    # fixing 2005-2009 data
    if period == "2005-2009":
        data = fix_2005_2009_data(data, variable_name)

    # loading the population data to add to the dataframe
    data = add_population(data, period)

    # creating a variable to record the period
    data["period"] = [period] * len(data)

    # make tracts into community areas
    data = get_community_areas(data, period)
        
    # adding data to the dictionary
    variable_tuple[0].append(data)

    return variable_tuple


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
    filename = pathlib.Path(__file__).parent / "clean_data" /name
    data.to_csv(filename, index=False)


def add_population(dataframe:pd, period:str):
    """
    Given a dataframe and a period of time, add a column recording the 
    corresponding population to each tract
    """
    population_file = "population_" + period + ".csv"
    popfile = pathlib.Path(__file__).parent / "raw_data" / period / population_file
    pop_data = pd.read_csv(popfile)
    
    # creating a variable to record the population
    if period == "2005-2009" or period == "2010-2014":
        dataframe["population"] = pop_data["B01001_001E"]
    if period == "2015-2019" or period == "2018-2022":
        dataframe["population"] = pop_data["B01003_001E"]
    
    return dataframe


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
                data.insert(name_column_index + 1, new, 0)
                continue
            data = combine_columns(new, old, data)
    
    return data


def combine_columns(new_name: str, old_names: list, dataframe: pd):
    """
    Combines columns in a dataframe into a new column
    """
    # change the first one in place so the dataframe stays pretty
    dataframe.rename(columns = {old_names[0] : new_name}, inplace = True)

    # add and drop the remaining columns to the renamed column
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
