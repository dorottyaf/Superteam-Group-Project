import pathlib
from conversion_dics import age_conversion, educ_conversion, income_conversion
from column_conversion import age_dictionary, educ_dictionary, \
    income_dictionary, ethnicity_dictionary, gender_dictionary, \
    household_dictionary, race_dictionary
import pandas as pd

filename = pathlib.Path(__file__).parent / "raw_data" / "2010-2014" / "educ_2010-2014.csv"
educ_data = pd.read_csv(filename)

print(educ_data)