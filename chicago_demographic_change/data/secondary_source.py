from data_analysis.geomatching import ZIP_CODES, COMM_AREAS, shape_matcher
import pathlib
import pandas as pd
import geopandas as gpd
import re


# Note that most of these datasets have year limitations tighter than ACS Data
# Business License and Building Permit groupings you may wish to avoid re-running
# cleaning functions on, as both are quite large.

CA_PATH = pathlib.Path(__file__).parents[1] / "data_analysis" / "Location Information" / "Boundaries - Community Areas (current)" / "geo_export_8fac6090-b29a-4cf4-b6ab-c66b0d4da44a.shp"

# String coding for cleaning:
YEARS = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]

PERIODS = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]

#DePaul-Specific String encodings
NOT_CHICAGO = ["COOK","CHICAGO","SUBURBS","Palatine/Barrington","Melrose Park/Maywood",\
               "Oak Park/Cicero","LaGrange/Burbank","Orland Park/Lemont",\
                "Oak Lawn/Blue Island","Oak Forest/Country Club Hills",\
                "Calumet City/Harvey","Chicago Heights/Park Forest",\
                "Arlington Heights/Wheeling","Winnetka/Northbrook",\
                "Hoffman Estates/Streamwood","Schaumburg","Mount Prospect/Elk Grove Village",\
                "Park Ridge/Des Plaines", "Evanston/Skokie","Elmwood Park/Franklin Park"]
DATA_TO_COMMUNITY = {
    "Chicago--Uptown/Rogers Park": ["ROGERS PARK", "UPTOWN", "EDGEWATER", "WEST RIDGE"],
    "Chicago--Lake View/Lincoln Park": ["LAKE VIEW", "LINCOLN PARK"],
    "Chicago--Lincoln Square/North Center": ["LINCOLN SQUARE", "NORTH CENTER"],
    "Chicago--Irving Park/Albany Park": ["ALBANY PARK", "IRVING PARK", "NORTH PARK"],
    "Chicago--Portage Park/Jefferson Park": ["JEFFERSON PARK", "PORTAGE PARK", "FOREST GLEN", "NORWOOD PARK", "EDISON PARK"],
    "Chicago--Austin/Belmont Cragin": ["AUSTIN", "BELMONT CRAGIN", "DUNNING", "MONTCLARE", "OHARE"],
    "Chicago--Logan Square/Avondale": ["AVONDALE", "LOGAN SQUARE", "HERMOSA"],
    "Chicago--Humboldt Park/Garfield Park": ["HUMBOLDT PARK", "EAST GARFIELD PARK", "WEST GARFIELD PARK"],
    "Chicago--West Town/Near West Side": ["NEAR WEST SIDE", "WEST TOWN", "LOOP", "NEAR NORTH SIDE", "SOUTH LAWNDALE", "NORTH LAWNDALE", "LOWER WEST SIDE", "NEAR SOUTH SIDE"],
    "Chicago--Bridgeport/Brighton Park": ["BRIDGEPORT", "BRIGHTON PARK", "MCKINLEY PARK", "ARMOUR SQUARE", "NEW CITY"],
    "Chicago--Gage Park/West Lawn": ["GAGE PARK", "WEST LAWN", "ARCHER HEIGHTS", "WEST ELSDON", "CHICAGO LAWN", "CLEARING", "GARFIELD RIDGE"],
    "Chicago--Englewood/Greater Grand Crossing": ["ENGLEWOOD", "GREATER GRAND CROSSING", "WEST ENGLEWOOD"],
    "Chicago--Bronzeville/Hyde Park": ["HYDE PARK", "FULLER PARK", "DOUGLAS", "GRAND BOULEVARD", "WASHINGTON PARK", "WOODLAWN", "KENWOOD", "OAKLAND"],
    "Chicago--Beverly/Morgan Park": ["BEVERLY", "MORGAN PARK", "MOUNT GREENWOOD"],
    "Chicago--Auburn Gresham/Chatham": ["AUBURN GRESHAM", "CHATHAM", "AVALON PARK", "BURNSIDE", "CALUMET HEIGHTS", "WASHINGTON HEIGHTS", "ASHBURN"],
    "Chicago--South Chicago/West Pullman": ["PULLMAN", "SOUTH CHICAGO", "WEST PULLMAN", "ROSELAND", "SOUTH SHORE", "RIVERDALE", "EAST SIDE", "HEGEWISCH", "SOUTH DEERING"],
}


# DePaul Housing Institute Pricing Index

def depaul_clean():
    """
    Does all the necessary cleaning and returns a clean dataframe
    """

    # load depaul file
    filename = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
    depaul = pd.read_csv(filename)

    depaul = community_fix(depaul)
    depaul = transpose(depaul)
    depaul = delete_irrelevant_years(depaul)
    depaul = combine_years(depaul)
    depaul = get_change_columns(depaul)

    out_filename = pathlib.Path(__file__).parent / "clean_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
    depaul.to_csv(out_filename, index = False)

def community_fix(dataframe:pd):
    """
    Rewrite the data to be based on community areas
    """
    for column in NOT_CHICAGO:
        dataframe = dataframe.drop(column, axis = 1)

    for column in dataframe:
        if column != "YEARQ":
            for comm_area in DATA_TO_COMMUNITY[column]:
                dataframe[comm_area] = dataframe[column]
            dataframe = dataframe.drop(column, axis = 1)
    
    return dataframe


def transpose(dataframe:pd):
    """
    Flip the dataframe so it becomes managable, clear up any confusion caused
    by transposing
    """
    dataframe = dataframe.T
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe[1:]
    dataframe.reset_index(inplace=True)
    dataframe.rename(columns = {"index": "community_area"}, inplace = True)

    return dataframe


def delete_irrelevant_years(dataframe:pd):
    """
    Delete the years not relevant to our project from the dataframe
    """
    for column in dataframe:
        if column == "community_area":
            continue
        if column[:4] < "2005":
            dataframe = dataframe.drop(column, axis = 1)
        if column[:4] > "2022":
            dataframe = dataframe.drop(column, axis = 1)
    
    return dataframe


def combine_years(dataframe:pd):
    """
    Combines the years in the dataframe so they show the average depaul index
    for the years we're interested in
    """
    for period in YEARS:
        dataframe[period] = 0
        divisor = 0
        for column in dataframe:
            if column in YEARS:
                continue
            if column[:4] >= period[:4] and column[:4] <= period[5:]:
                dataframe[period] = dataframe[period] + dataframe[column]
                divisor += 1
        dataframe[period] = dataframe[period] / divisor


    for column in dataframe:
        if column not in YEARS and column != "community_area":
            dataframe = dataframe.drop(column, axis = 1)
    
    return dataframe


def get_change_columns(dataframe:pd):
    """
    Calculates the absolute change between two time periods and sorts them into
    a high, medium, or low bucket
    """
    change_columns = []

    # calculating change over time columns
    for period1, period2 in PERIODS:
        text = period1 + " to " + period2
        change_columns.append(text)
        dataframe[text] = abs(dataframe[period2] - dataframe[period1])

    # Converting change over time to bins
    for column in change_columns:
        mid_bound = dataframe[column].quantile(q = 0.333, interpolation = "lower")
        high_bound = dataframe[column].quantile(q = 0.666, interpolation = "lower")
        lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
        dataframe[column] = pd.cut(dataframe[column], bins = lmh_bins, labels = ["low", "medium", "high"])

    return dataframe

### City of Chicago Business License Counts

def city_blc_clean():

    city_blc_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Business_Licenses_20240217.csv"
    blc_df = pd.read_csv(city_blc_path)
    
    blc_df["APPLICATION CREATED DATE"] = blc_df["APPLICATION CREATED DATE"].astype(str)
    blc_df["APPLICATION CREATED DATE"] = blc_df["APPLICATION CREATED DATE"].apply(date_clean)
    blc_df = blc_df.drop(blc_df[blc_df["APPLICATION CREATED DATE"] == "rm"].index)

    data_years = set(blc_df["APPLICATION CREATED DATE"])
    counts_list = []
    for year in data_years:
        year_df = blc_df[blc_df["APPLICATION CREATED DATE"] == year]
        area_counts = year_df["ZIP CODE"].value_counts()
        for area in area_counts.index:
            key = str(area)
            counts_list.append((year, key, area_counts[area],))
    
    matching_dict = shape_matcher(ZIP_CODES, COMM_AREAS)
    inverted_match_dict = {}
    for key in matching_dict:
        for zip in matching_dict[key]:
            inverted_match_dict[zip] = key

    # Building a clean Dataframe
    ref_dict, row_series = colswitch_tools()
    year_columns = blc_df["APPLICATION_START_DATE"].unique().astype(str)
    clean_df = pd.DataFrame(0.0, index = row_series, columns = year_columns)

    for tup in counts_list:
        year, zip_key, count = tup
        comm_area = inverted_match_dict[zip_key]
        clean_df.loc[comm_area, year] = count
    
    clean_df = city_column_aggregator(clean_df)

    clean_df.insert(0, "community_area" , clean_df.index)
    out_filename = pathlib.Path(__file__).parent / "clean_data" / "Secondary Data" / "City_BLC_Applications.csv"
    clean_df.to_csv(out_filename, index = False)
    

# City of Chicago Building Permit Counts

def city_permit_clean():
    ''' 
    Cleaning Process:
    - Imported data as a pandas dataframe
    - Base field cleaning to aggregate date by year.
    - Build a counts list for each community area by year for the new dataframe
    - Assemble a clean dataframe and insert counts from the list
    - Build aggregated columns to match to census data, and columns for the 
        differences between time periods
    - Used quantile markers to split data into 3 levels of change
    - Assigned each comm area/year to a category based on amount of change

    Output: .csv placed in Secondary Data: clean_data of the cleaned dataframe
        with columns indicating the level of change between time periods of interest.
    '''
    city_permit_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Building_Permits_20240217.csv"
    bp_df = pd.read_csv(city_permit_path)

    bp_df["APPLICATION_START_DATE"] = bp_df["APPLICATION_START_DATE"].astype(str)
    bp_df["APPLICATION_START_DATE"] = bp_df["APPLICATION_START_DATE"].apply(date_clean)
    bp_df = bp_df.drop(bp_df[bp_df["APPLICATION_START_DATE"] == "rm"].index)

    # Building a list from which to fill out a clean dataframe.
    data_years = set(bp_df["APPLICATION_START_DATE"])
    counts_list = []
    for year in data_years:
        year_df = bp_df[bp_df["APPLICATION_START_DATE"] == year]
        area_counts = year_df["COMMUNITY_AREA"].value_counts()
        for area in area_counts.index:
            key = str(area)
            counts_list.append((year, key, area_counts[area],))

    # Building a clean Dataframe
    ref_dict, row_series = colswitch_tools()
    year_columns = bp_df["APPLICATION_START_DATE"].unique().astype(str)
    clean_df = pd.DataFrame(0.0, index = row_series, columns = year_columns)

    for num in counts_list:
        year, ca_num, count = num
        ca_num = str(int(float(ca_num)))
        if ca_num != "0":
            comm_area = ref_dict[ca_num]
            clean_df.loc[comm_area, year] = count

    #Writes Aggregated Columns
    clean_df["2005-2009"] = (clean_df["2005"] + clean_df["2006"] + clean_df["2007"]
                                + clean_df["2008"] + clean_df["2009"])/5
    clean_df["2010-2014"] = (clean_df["2010"] + clean_df["2011"] + clean_df["2012"]
                                + clean_df["2013"] + clean_df["2014"])/5
    clean_df["2015-2019"] = (clean_df["2015"] + clean_df["2016"] + clean_df["2017"]
                                + clean_df["2018"] + clean_df["2019"])/5
    clean_df["2018-2022"] = (clean_df["2018"] + clean_df["2019"] + clean_df["2020"]
                                + clean_df["2021"] + clean_df["2022"])/5
    
    # Builds change over time columns
    change_columns = []
    for period1, period2 in PERIODS:
        text = period1 + " to " + period2
        change_columns.append(text)
        clean_df[text] = abs(clean_df[period2] - clean_df[period1])

    #Converts change over time columns to bins
    for column in change_columns:
        mid_bound = clean_df[column].quantile(q = 0.333, interpolation = "lower")
        high_bound = clean_df[column].quantile(q = 0.666, interpolation = "lower")
        lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
        clean_df[column] = pd.cut(clean_df[column], bins = lmh_bins, labels = ["low", "medium", "high"])

    clean_df.insert(0, "community_area" , clean_df.index)
    out_filename = pathlib.Path(__file__).parent / "clean_data" / "Secondary Data" / "City_Permit_Applications.csv"
    clean_df.to_csv(out_filename, index = False)


# City of Chicago Vacant and Abandoned Building Violations

def city_vacant_clean():
    '''
    Cleaning Process:
    - Imported 2 dataframes: comm_area polygons and the vacant buildings file as
        geopandas dataframes.
    - Base field cleaning to aggregate date by year, and rebuilding a geometry
        for the location of each vacant building violation.
    - Assign each violation to a community area with shape matching
    - Build a counts list for each community area by year for the new dataframe
    - Assemble a clean dataframe and insert counts from the list
    - Build aggregated columns to match to census data, and columns for the 
        differences between time periods
    - Used quantile markers to split data into 3 levels of change
    - Assigned each comm area/year to a category based on amount of change

    Output: .csv placed in Secondary Data: clean_data of the cleaned dataframe
        with columns indicating the level of change between time periods of interest.
    
    '''
    city_vacant_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Vacant_and_Abandoned_Buildings_-_Violations_20240217.csv"
    ca_polys = gpd.read_file(CA_PATH)
    build_vio = gpd.read_file(city_vacant_path)
    ca_polys = ca_polys.to_crs("WGS84")
    
    # Cleaning date fields
    build_vio["Issued Date"] = build_vio["Issued Date"].astype(str)
    build_vio["Issued Date"] = build_vio["Issued Date"].apply(date_clean)
    build_vio = build_vio.drop(build_vio[build_vio["Issued Date"] == "rm"].index)

    #Rebuilding geometry due to type change failing w/ Location
    build_vio["Longitude"] = pd.to_numeric(build_vio["Longitude"])
    build_vio["Latitude"] = pd.to_numeric(build_vio["Latitude"])
    build_vio["geometry"] = gpd.points_from_xy(build_vio["Longitude"], build_vio["Latitude"], crs = "WGS84")
    
    build_vio["Comm_Area"] = None
    #Inefficient, but somewhat required for checking each point against many shapes
    for ca_index, ca_row in ca_polys.iterrows():
        check_series = build_vio.within(ca_row["geometry"])
        for b_index, b_row in build_vio.iterrows():
            if check_series[b_index]:
                build_vio.loc[b_index,"Comm_Area"] = ca_row["community"]
    
    data_years = set(build_vio["Issued Date"])
    counts_list = []
    for year in data_years:
        year_df = build_vio[build_vio["Issued Date"] == year]
        area_counts = year_df["Comm_Area"].value_counts()
        for area in area_counts.index:
            key = str(area)
            counts_list.append((year, key, area_counts[area],))

    ref_dict, row_series = colswitch_tools()
    city_columns = build_vio["Issued Date"].unique().astype(str)
    clean_df = pd.DataFrame(0.0, index = row_series, columns = city_columns)

    for num in counts_list:
        year, comm_area, count = num
        clean_df.loc[comm_area, year] = count
    
    # Missing 2010- adjusting for more comparisons
    clean_df.insert(0, "community_area" , clean_df.index)
    clean_df["2010-2014"] = (clean_df["2011"] + clean_df["2012"]
                                + clean_df["2013"] + clean_df["2014"])/4
    clean_df["2015-2019"] = (clean_df["2015"] + clean_df["2016"] + clean_df["2017"]
                                + clean_df["2018"] + clean_df["2019"])/5
    clean_df["2018-2022"] = (clean_df["2018"] + clean_df["2019"] + clean_df["2020"]
                                + clean_df["2021"] + clean_df["2022"])/5
    
    change_columns = ["2010-2014 to 2015-2019", "2010-2014 to 2018-2022", 
                      "2015-2019 to 2018-2022"]
    clean_df["2010-2014 to 2015-2019"] = abs(clean_df["2015-2019"]- clean_df["2010-2014"])
    clean_df["2010-2014 to 2018-2022"] = abs(clean_df["2018-2022"]- clean_df["2010-2014"])
    clean_df["2015-2019 to 2018-2022"] = abs(clean_df["2018-2022"]- clean_df["2015-2019"])
    
    for column in change_columns:
        mid_bound = clean_df[column].quantile(q = 0.333, interpolation = "lower")
        high_bound = clean_df[column].quantile(q = 0.666, interpolation = "lower")
        lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
        clean_df[column] = pd.cut(clean_df[column], bins = lmh_bins, labels = ["low", "medium", "high"])

    out_filename = pathlib.Path(__file__).parent / "clean_data" / "Secondary Data" / "City_Vacant_Abandoned.csv"
    clean_df.to_csv(out_filename, index = False)

# LCBH Eviction Data
    
def eviction_clean():
    '''
    Cleaning Process:
    - Imported csv as pandas dataframe
    - Set up a clean dataframe with Community Area rows, year columns
    - Transcribed data into frame
    - Built 5-year aggregations to match Census Tract data
    - Used quantile markers to split data into 3 levels of change
    - Assigned each comm area/year to a category based on amount of change

    Output: .csv placed in Secondary Data: clean_data of the cleaned dataframe
        with columns indicating the level of change between time periods of interest.
    '''
    eviction_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "eviction_data_comm_area.csv"
    df = pd.read_csv(eviction_path)

    # Sets up the clean dataframe with empty values
    clean_df_row = df["area_name"].str.upper().unique()
    clean_df_col = df["filing_year"].unique()
    clean_df = pd.DataFrame(0.0, columns = clean_df_col, index = clean_df_row)

    # Transcribes data into Comm_area * Year format
    for index, num in df["eviction_filings_rate"].items():
        year = df["filing_year"][index]
        comm_area = df["area_name"][index]

        clean_df.loc[comm_area, year] = num

    # Aggregated Columns
    clean_df["2010-2014"] = (clean_df[2010] + clean_df[2011] + clean_df[2012]
                              + clean_df[2013] + clean_df[2014])/5
    clean_df["2015-2019"] = (clean_df[2015] + clean_df[2016] + clean_df[2017]
                              + clean_df[2018] + clean_df[2019])/5
    
    clean_df["2010-2014 to 2015-2019"] = abs(clean_df["2015-2019"]- clean_df["2010-2014"])
    clean_df.insert(0, "community_area" , clean_df.index)

    mid_bound = clean_df["2010-2014 to 2015-2019"].quantile(q = 0.333, interpolation = "lower")
    high_bound = clean_df["2010-2014 to 2015-2019"].quantile(q = 0.666, interpolation = "lower")
    lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
    clean_df["2010-2014 to 2015-2019"] = pd.cut(
        clean_df["2010-2014 to 2015-2019"], 
        bins = lmh_bins, labels = ["low", "medium", "high"])

    out_filename = pathlib.Path(__file__).parent / "clean_data" / "Secondary Data" / "LCBH_Evictions.csv"
    clean_df.to_csv(out_filename, index = False)

    

# Cleaning Helper Functions

def date_clean(date):
    '''
    Used to remove data outside of the years relevant to the census data.
    '''
    date_year = re.search(r"\d{4}", date)
    if date_year:
        date = date_year.group(0)
        date_year_num = int(date)
        if date_year_num < 2005 or date_year_num > 2023:
            date = "rm"
    else:
        date = "rm"

    return date


def colswitch_tools():
    '''
    Builds several small components related to community areas for use in cleaning

    Outputs:
        name_num_dict: dictionary of community areas mapped to City of Chicago numeric
            indicators for those CAs
        row_series: geopandas series of community area names
    '''
    df = gpd.read_file(CA_PATH)   
    name_num_dict = {}
    for index, row in df.iterrows():
        name_num_dict[df["area_num_1"][index]] = df["community"][index]
    row_series = df["community"]

    return name_num_dict, row_series

def city_column_aggregator(clean_df):
    #Writes Aggregated Columns
    clean_df["2005-2009"] = (clean_df["2005"] + clean_df["2006"] + clean_df["2007"]
                                + clean_df["2008"] + clean_df["2009"])/5
    clean_df["2010-2014"] = (clean_df["2010"] + clean_df["2011"] + clean_df["2012"]
                                + clean_df["2013"] + clean_df["2014"])/5
    clean_df["2015-2019"] = (clean_df["2015"] + clean_df["2016"] + clean_df["2017"]
                                + clean_df["2018"] + clean_df["2019"])/5
    clean_df["2018-2022"] = (clean_df["2018"] + clean_df["2019"] + clean_df["2020"]
                                + clean_df["2021"] + clean_df["2022"])/5
    
    # Builds change over time columns
    change_columns = []
    for period1, period2 in PERIODS:
        text = period1 + " to " + period2
        change_columns.append(text)
        clean_df[text] = abs(clean_df[period2] - clean_df[period1])

    #Converts change over time columns to bins
    for column in change_columns:
        mid_bound = clean_df[column].quantile(q = 0.333, interpolation = "lower")
        high_bound = clean_df[column].quantile(q = 0.666, interpolation = "lower")
        lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
        clean_df[column] = pd.cut(clean_df[column], bins = lmh_bins, labels = ["low", "medium", "high"])

    return clean_df

######## Functions Running Secondary Sources #########

depaul_clean()
#city_blc_clean()
city_permit_clean()
city_vacant_clean()
eviction_clean()