from .clean_process import get_one_dataset, make_combined_datasets
from .column_conversion import age_dictionary, educ_dictionary, income_dictionary, \
    ethnicity_dictionary, gender_dictionary, household_dictionary, race_dictionary
from .combination_dicts import age_categories, income_categories, household_categories

# list of years and variables
years = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]
# dictionary of the datasets for a variable, and their conversion dictionaries
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

for name, tuples in variables.items():
    for period in years:
        tuples = get_one_dataset(period, name, tuples)
    make_combined_datasets(name, tuples)
