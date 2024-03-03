# Dictionaries associating the census code with their definition
# KEYS are the original code
# VALUES are the definitions / new variable names to be used

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