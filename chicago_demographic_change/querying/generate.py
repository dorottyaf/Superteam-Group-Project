from .APIquery import make_pull, make_pull_2022

# Import our list of census variables
from .querying_constants import (
    gender_vars,
    race_vars,
    age_vars,
    educ_vars,
    income_vars,
    household_vars,
    ethnicity_vars,
    population_1922,
    population_0914,
    age_2009_vars,
    income_2009_vars,
    educ_2009_vars,
)

# NOTE: Not a function because variable arguments change year by year

# 2015-2019 pulls
make_pull(
    2019,
    gender_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/gender_2015-2019.csv",
)
make_pull(
    2019,
    race_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/race_2015-2019.csv",
)
make_pull(
    2019,
    age_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/age_2015-2019.csv",
)
make_pull(
    2019,
    educ_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/educ_2015-2019.csv",
)
make_pull(
    2019,
    income_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/income_2015-2019.csv",
)
make_pull(
    2019,
    household_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/household_2015-2019.csv",
)
make_pull(
    2019,
    ethnicity_vars,
    "chicago_demographic_change/data/raw_data/2015-2019/ethnicity_2015-2019.csv",
)
make_pull(
    2019,
    population_1922,
    "chicago_demographic_change/data/raw_data/2015-2019/population_2015-2019.csv",
)

# 2010-2014 pulls
make_pull(
    2014,
    gender_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/gender_2010-2014.csv",
)
make_pull(
    2014,
    race_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/race_2010-2014.csv",
)
make_pull(
    2014,
    age_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/age_2010-2014.csv",
)
make_pull(
    2014,
    educ_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/educ_2010-2014.csv",
)
make_pull(
    2014,
    income_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/income_2010-2014.csv",
)
make_pull(
    2014,
    household_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/household_2010-2014.csv",
)
make_pull(
    2014,
    ethnicity_vars,
    "chicago_demographic_change/data/raw_data/2010-2014/ethnicity_2010-2014.csv",
)
make_pull(
    2014,
    population_0914,
    "chicago_demographic_change/data/raw_data/2010-2014/population_2010-2014.csv",
)

# 2005-2009 pulls
make_pull(
    2009,
    gender_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/gender_2005-2009.csv",
)
make_pull(
    2009,
    race_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/race_2005-2009.csv",
)
make_pull(
    2009,
    age_2009_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/age_2005-2009.csv",
)
make_pull(
    2009,
    educ_2009_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/educ_2005-2009.csv",
)
make_pull(
    2009,
    income_2009_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/income_2005-2009.csv",
)
make_pull(
    2009,
    household_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/household_2005-2009.csv",
)
make_pull(
    2009,
    ethnicity_vars,
    "chicago_demographic_change/data/raw_data/2005-2009/ethnicity_2005-2009.csv",
)
make_pull(
    2009,
    population_0914,
    "chicago_demographic_change/data/raw_data/2005-2009/population_2005-2009.csv",
)

# 2018-2022 pulls
make_pull_2022(
    gender_vars,
    "chicago_demographic_change/data/raw_data/2018-2022/gender_2018-2022.csv",
)
make_pull_2022(
    race_vars, "chicago_demographic_change/data/raw_data/2018-2022/race_2018-2022.csv"
)
make_pull_2022(
    age_vars, "chicago_demographic_change/data/raw_data/2018-2022/age_2018-2022.csv"
)
make_pull_2022(
    educ_vars, "chicago_demographic_change/data/raw_data/2018-2022/educ_2018-2022.csv"
)
make_pull_2022(
    income_vars,
    "chicago_demographic_change/data/raw_data/2018-2022/income_2018-2022.csv",
)
make_pull_2022(
    household_vars,
    "chicago_demographic_change/data/raw_data/2018-2022/household_2018-2022.csv",
)
make_pull_2022(
    ethnicity_vars,
    "chicago_demographic_change/data/raw_data/2018-2022/ethnicity_2018-2022.csv",
)
make_pull_2022(
    population_1922,
    "chicago_demographic_change/data/raw_data/2018-2022/population_2018-2022.csv",
)
