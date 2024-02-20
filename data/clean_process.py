import pathlib
from conversion_dics import age_conversion, educ_conversion, income_conversion
from column_conversion import age_dictionary, educ_dictionary, income_dictionary, \
    ethnicity_dictionary, gender_dictionary, household_dictionary, race_dictionary

import pandas as pd


# list of years and variables
years = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]
# dictionary of the datasets for a variable, and their conversion dictionary
# in a tuple
variables = {
    "age": ([], age_dictionary),
    "ethnicity": ([], ethnicity_dictionary),
    "household": ([], household_dictionary),
    "educ": ([], educ_dictionary),
    "gender": ([], gender_dictionary),
    "income": ([], income_dictionary),
    "race": ([], race_dictionary),
}
     

        
def load_in_datasets(period:str, variable_name: str, variable_tuple: tuple):
    """
    Load in the raw data, append some missing columns, and append it to the list
    in its corresponding dictionary
    """
    current_file = variable_name + "_" + period + ".csv"
    filename = pathlib.Path(__file__).parent / "raw_data" / period / current_file
    data = pd.read_csv(filename)

    # loading the population data to add to the dataframe
    population_file = "population_" + period + ".csv"
    popfile = pathlib.Path(__file__).parent / "raw_data" / period / population_file
    pop_data = pd.read_csv(popfile)

    # fixing 2005-2009 data
    if period == "2005-2009":
        if variable_name == "age":
            for new, old in age_conversion.items():
                data[new] = 0
                for instance in old:
                    data[new] = data[new] + data[instance]
                    data = data.drop(instance, axis = "columns")
            
        if variable_name == "educ":
            for new, old in educ_conversion.items():
                data[new] = 0
                for instance in old:
                    data[new] = data[new] + data[instance]
                    data = data.drop(instance, axis = "columns")

        if variable_name == "income":
            for new, old in income_conversion.items():
                if new == "B06010_002E":
                    data[new] = "na"
                    continue
                data[new] = 0
                for instance in old:
                    data[new] = data[new] + data[instance]
                    data = data.drop(instance, axis = "columns")
        
    # creating a variable to record the population
    if period == "2005-2009" or period == "2010-2014":
        data["population"] = pop_data["B00001_001E"]
    if period == "2015-2019" or period == "2018-2022":
        data["population"] = pop_data["B01003_001E"]

    # creating a variable to record the period
    data["period"] = [period] * len(data)
        
    # adding data to the dictionary
    variable_tuple[0].append(data)

    return variable_tuple


def make_combined_datasets(variable_name: str, variable_tuple: tuple):
    """
    Combine the different datasets for a variable into one large dataset
    """
    data = pd.concat(variable_tuple[0])
    data.rename(columns = variable_tuple[1], inplace = True)
    name = variable_name + "_data.csv"
    filename = pathlib.Path(__file__).parent / "clean_data" / name
    data.to_csv(filename)


for name, tuples in variables.items():
    for period in years:
        tuples = load_in_datasets(period, name, tuples)
    make_combined_datasets(name, tuples)