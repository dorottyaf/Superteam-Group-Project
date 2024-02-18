import pathlib
from conversion_dics import age_conversion, educ_conversion, income_conversion

import pandas as pd

age_dictionary = {
    "B07001_002E": "1-4",
    "B07001_003E": "5-17",
    "B07001_004E": "18-19",
    "B07001_005E": "20-24",
    "B07001_006E": "25-29",
    "B07001_007E": "30-34",
    "B07001_008E": "35-39",
    "B07001_009E": "40-44",
    "B07001_010E": "45-49",
    "B07001_011E": "50-54",
    "B07001_012E": "55-59",
    "B07001_013E": "60-64",
    "B07001_014E": "65-69",
    "B07001_015E": "70-74",
    "B07001_016E": "75+"
}

educ_dictionary = {
    "B06009_002E": "no_hs",
    "B06009_003E": "hs",
    "B06009_004E": "some_college",
    "B06009_005E": "bachelors",
    "B06009_006E": "graduate"
}

income_dictionary = {
    "B06010_002E": "no_income",
    "B06010_004E": "1-10k",
    "B06010_005E": "10-15k",
    "B06010_006E": "15-25k",
    "B06010_007E": "25-35k",
    "B06010_008E": "35-50k",
    "B06010_009E": "50-65k",
    "B06010_010E": "65-75k",
    "B06010_011E": "75k+"
    }

ethnicity_dictionary = {
    "B03001_002E": "not_hispanic",
    "B03001_003E": "hispanic"
}

gender_dictionary = {
    "B01001_026E" : "female"
}

household_dictionary = {
    "B19001_002E": "less_than_10k",
    "B19001_003E": "10-15k",
    "B19001_004E": "15-20k",
    "B19001_005E": "20-25k",
    "B19001_006E": "25-30k",
    "B19001_007E": "30-35k",
    "B19001_008E": "35-40k",
    "B19001_009E": "40-45k",
    "B19001_010E": "45-50k",
    "B19001_011E": "50-60k",
    "B19001_012E": "60-75k",
    "B19001_013E": "75-100k",
    "B19001_014E": "100-125k",
    "B19001_015E": "125-150k",
    "B19001_016E": "150-200k",
    "B19001_017E": "200k+"
}

race_dictionary = {
    "B02001_002E": "white",
    "B02001_003E": "black",
    "B02001_004E": "native",
    "B02001_005E": "asian",
    "B02001_006E": "hawaii_pacific",
    "B02001_007E": "other",
    "B02001_008E": "two_or_more"
}

# list of years and variables
years = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]
variables = {
    "age": [], 
    "ethnicity": [], 
    "household": [], 
    "educ": [], 
    "gender": [], 
    "income": [], 
    "race": []
}

# loading all the data into their corresponding dictionary
for period in years:
    for name, variable in variables.items():
        current_file = name + "_" + period + ".csv"
        filename = pathlib.Path(__file__).parent / "raw_data" / period / current_file
        data = pd.read_csv(filename)

        # loading the popoulation data to add to the dataframe
        population_file = "population_" + period + ".csv"
        popfile = pathlib.Path(__file__).parent / "raw_data" / period / population_file
        pop_data = pd.read_csv(popfile)

        # fixing 2005-2009 data
        if period == "2005-2009":
            if name == "age":
                for new, old in age_conversion.items():
                    data[new] = 0
                    for instance in old:
                        data[new] = data[new] + data[instance]
                        data = data.drop(instance, axis = "columns")
            
            if name == "educ":
                for new, old in educ_conversion.items():
                    data[new] = 0
                    for instance in old:
                        data[new] = data[new] + data[instance]
                        data = data.drop(instance, axis = "columns")

            if name == "income":
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
        variable.append(data)

# combining the datasets for each value
# will probably become a function at some point
age_data = pd.concat(variables["age"])
age_data.rename(columns = age_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "age_data.csv"
age_data.to_csv(filename)

ethnicity_data = pd.concat(variables["ethnicity"])
ethnicity_data.rename(columns = ethnicity_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "ethnicity_data.csv"
ethnicity_data.to_csv(filename)


household_data = pd.concat(variables["household"])
household_data.rename(columns = household_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "household_data.csv"
household_data.to_csv(filename)

educ_data = pd.concat(variables["educ"])
educ_data.rename(columns = educ_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "educ_data.csv"
educ_data.to_csv(filename)

gender_data = pd.concat(variables["gender"])
gender_data.rename(columns = gender_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "gender_data.csv"
gender_data.to_csv(filename)

income_data = pd.concat(variables["income"])
income_data.rename(columns = income_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "income_data.csv"
income_data.to_csv(filename)

race_data = pd.concat(variables["race"])
race_data.rename(columns = race_dictionary, inplace = True)
filename = pathlib.Path(__file__).parent / "clean_data" / "race_data.csv"
race_data.to_csv(filename)

