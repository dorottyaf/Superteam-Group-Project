from APIquery import make_pull, make_pull_2022

gender_vars = ("NAME", "B01001_026E")

race_vars = ("NAME", "B02001_002E", "B02001_003E", "B02001_004E", "B02001_005E", 
             "B02001_006E", "B02001_007E", "B02001_008E")

age_vars = ("NAME", "B07001_002E", "B07001_003E", "B07001_004E", "B07001_005E", 
            "B07001_006E", "B07001_007E", "B07001_008E", "B07001_009E", "B07001_010E", 
            "B07001_011E", "B07001_012E", "B07001_013E", "B07001_014E", "B07001_015E", 
            "B07001_016E")

educ_vars = ("NAME", "B06009_002E", "B06009_003E", "B06009_004E", "B06009_005E", 
             "B06009_006E")

income_vars = ("NAME", "B06010_002E", "B06010_004E", "B06010_005E", "B06010_006E", 
               "B06010_007E", "B06010_008E", "B06010_009E", "B06010_010E", "B06010_011E")

household_vars = ("NAME", "B19001_002E", "B19001_003E", "B19001_004E", "B19001_005E", 
                  "B19001_006E", "B19001_007E", "B19001_008E", "B19001_009E", 
                  "B19001_010E", "B19001_011E", "B19001_012E", "B19001_013E", 
                  "B19001_014E", "B19001_015E", "B19001_016E", "B19001_017E",)

ethnicity_vars = ("NAME", "B03001_002E", "B03001_003E")

age_2009_vars = ("NAME", "B01001_003E", "B01001_004E", "B01001_005E", "B01001_006E", 
                 "B01001_007E", "B01001_008E", "B01001_009E", "B01001_010E", 
                 "B01001_011E", "B01001_012E", "B01001_013E", "B01001_014E", 
                 "B01001_015E", "B01001_016E", "B01001_017E", "B01001_018E", 
                 "B01001_019E", "B01001_020E", "B01001_021E", "B01001_022E", 
                 "B01001_023E", "B01001_024E", "B01001_025E",
                 "B01001_027E", "B01001_028E", "B01001_029E", "B01001_030E", 
                 "B01001_031E", "B01001_032E", "B01001_033E", "B01001_034E", 
                 "B01001_035E", "B01001_036E", "B01001_037E", "B01001_038E", 
                 "B01001_039E", "B01001_040E", "B01001_041E", "B01001_042E", 
                 "B01001_043E", "B01001_044E", "B01001_045E", "B01001_046E", 
                 "B01001_047E", "B01001_048E", "B01001_049E")

less_than = ["NAME", "B15001_004E", "B15001_005E", "B15001_012E", "B15001_013E", 
             "B15001_020E", "B15001_021E", "B15001_028E", "B15001_029E", 
             "B15001_036E", "B15001_037E", "B15001_045E", "B15001_046E", 
             "B15001_053E", "B15001_054E", "B15001_061E", "B15001_062E", 
             "B15001_069E", "B15001_070E", "B15001_077E", "B15001_078E"]

hs = ["B15001_006E", "B15001_014E", "B15001_022E", "B15001_030E", 
             "B15001_038E", "B15001_047E", "B15001_055E", "B15001_063E", 
             "B15001_071E", "B15001_079E"]

some_coll = ["B15001_007E", "B15001_008E", "B15001_015E", "B15001_016E", 
             "B15001_023E", "B15001_024E", "B15001_031E", "B15001_032E", 
             "B15001_039E", "B15001_040E", "B15001_048E", "B15001_049E", 
             "B15001_056E", "B15001_057E", "B15001_064E", "B15001_065E", 
             "B15001_072E", "B15001_073E", "B15001_080E", "B15001_081E"]

bachelors = ["B15001_009E", "B15001_017E", "B15001_025E", "B15001_033E", 
             "B15001_041E", "B15001_050E", "B15001_058E", "B15001_066E", 
             "B15001_074E", "B15001_082E"]

grad = ["B15001_010E", "B15001_018E", "B15001_026E", "B15001_034E", 
             "B15001_042E", "B15001_051E", "B15001_059E", "B15001_067E", 
             "B15001_075E", "B15001_083E"]

educ_2009_vars = tuple(less_than + hs + some_coll + bachelors + grad)

income_2009_vars = ("NAME", "B08119_002E", "B08119_003E", "B08119_004E", "B08119_005E", "B08119_006E", "B08119_007E", "B08119_008E", "B08119_009E")

# These are defined separately because the years have different variable codings
# Will be joined with respective datasets in cleaning
population_0914 = ("NAME", "B01001_001E")
population_1922 = ("NAME", "B01003_001E")

make_pull(2019, gender_vars, "data/raw_data/2015-2019/gender_2015-2019.csv")
make_pull(2019, race_vars, "data/raw_data/2015-2019/race_2015-2019.csv")
make_pull(2019, age_vars, "data/raw_data/2015-2019/age_2015-2019.csv")
make_pull(2019, educ_vars, "data/raw_data/2015-2019/educ_2015-2019.csv")
make_pull(2019, income_vars, "data/raw_data/2015-2019/income_2015-2019.csv")
make_pull(2019, household_vars, "data/raw_data/2015-2019/household_2015-2019.csv")
make_pull(2019, ethnicity_vars, "data/raw_data/2015-2019/ethnicity_2015-2019.csv")
make_pull(2019, population_1922, "data/raw_data/2015-2019/population_2015-2019.csv")

make_pull(2014, gender_vars, "data/raw_data/2010-2014/gender_2010-2014.csv")
make_pull(2014, race_vars, "data/raw_data/2010-2014/race_2010-2014.csv")
make_pull(2014, age_vars, "data/raw_data/2010-2014/age_2010-2014.csv")
make_pull(2014, educ_vars, "data/raw_data/2010-2014/educ_2010-2014.csv")
make_pull(2014, income_vars, "data/raw_data/2010-2014/income_2010-2014.csv")
make_pull(2014, household_vars, "data/raw_data/2010-2014/household_2010-2014.csv")
make_pull(2014, ethnicity_vars, "data/raw_data/2010-2014/ethnicity_2010-2014.csv")
make_pull(2014, population_0914, "data/raw_data/2010-2014/population_2010-2014.csv")

make_pull(2009, gender_vars, "data/raw_data/2005-2009/gender_2005-2009.csv")
make_pull(2009, race_vars, "data/raw_data/2005-2009/race_2005-2009.csv")
make_pull(2009, age_2009_vars, "data/raw_data/2005-2009/age_2005-2009.csv")
make_pull(2009, educ_2009_vars, "data/raw_data/2005-2009/educ_2005-2009.csv")
make_pull(2009, income_2009_vars, "data/raw_data/2005-2009/income_2005-2009.csv")
make_pull(2009, household_vars, "data/raw_data/2005-2009/household_2005-2009.csv")
make_pull(2009, ethnicity_vars, "data/raw_data/2005-2009/ethnicity_2005-2009.csv")
make_pull(2009, population_0914, "data/raw_data/2005-2009/population_2005-2009.csv")

make_pull_2022(gender_vars, "data/raw_data/2018-2022/gender_2018-2022.csv")
make_pull_2022(race_vars, "data/raw_data/2018-2022/race_2018-2022.csv")
make_pull_2022(age_vars, "data/raw_data/2018-2022/age_2018-2022.csv")
make_pull_2022(educ_vars, "data/raw_data/2018-2022/educ_2018-2022.csv")
make_pull_2022(income_vars, "data/raw_data/2018-2022/income_2018-2022.csv")
make_pull_2022(household_vars, "data/raw_data/2018-2022/household_2018-2022.csv")
make_pull_2022(ethnicity_vars, "data/raw_data/2018-2022/ethnicity_2018-2022.csv")
make_pull_2022(population_1922, "data/raw_data/2018-2022/population_2018-2022")