import pathlib
import pandas as pd
import geopandas as gpd
import json
import re

CA_PATH = pathlib.Path(__file__).parents[1] / "data_analysis" / "Location Information" / "Boundaries - Community Areas (current)" / "geo_export_8fac6090-b29a-4cf4-b6ab-c66b0d4da44a.shp"

# Note that most of these datasets have year limitations tighter than ACS Data
# Business License and Building Permit groupings cut down locally to shareable
# csvs of counts, have 1.1m and 750k records respectively

# DePaul Housing Institute Pricing Index
# UnConverted .xls file for if people need contextual information from the data
def depaul_import_raw():
    depaul_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
    df = pd.read_csv(depaul_path)
    return df

### City of Chicago Business License Counts ### DEPRECATED FOR NOW DUE TO PITA
'''
def city_blc_clean():
    Outputs a dictionary with not ideal keys, but year/community area counts of 
    business license applications. Not sure if the data in the early years is any good.
    city_blc_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Business_Licenses_20240217.csv"
    blc_df = pd.read_csv(city_blc_path)

    blc_df["APPLICATION CREATED DATE"] = blc_df["APPLICATION CREATED DATE"].astype(str)
    blc_df["APPLICATION CREATED DATE"] = blc_df["APPLICATION CREATED DATE"].apply(date_clean)
    blc_df = blc_df.drop(blc_df[blc_df.APPLICATION CREATED DATE == "rm"].index)

    data_years = set(blc_df["APPLICATION CREATED DATE"])
    counts_dict = {}

    for year in data_years:
        year_df = blc_df[blc_df["APPLICATION CREATED DATE"] == year]
        area_counts = year_df["ZIP CODE"].value_counts()
        for area in area_counts.index:
            key = str(year + ", " + str(area))
            counts_dict[key] = area_counts[area]
    #Need to add proper filepath
    with open("raw_data\Secondary Data\license_clean.json", "w") as readout:
        json.dump(counts_dict, readout)

    return counts_dict #Need to print to a csv somewhere, perhaps.
    '''



def city_blc_import_raw():
    ''' DATA FILE NOT UPLOADED, DO NOT USE (YET)'''
    city_blc_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Business_Licenses_20240217.csv"
    blc_df = pd.read_csv(city_blc_path)
    return blc_df

# City of Chicago Building Permit Counts

def city_permit_clean():
    ''' Outputs a dictionary with not ideal keys, but year/community area counts of 
    building permit applications. Not sure if the data in the early years is any good.
    '''
    city_permit_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Building_Permits_20240217.csv"
    bp_df = pd.read_csv(city_permit_path)

    bp_df["APPLICATION_START_DATE"] = bp_df["APPLICATION_START_DATE"].astype(str)
    bp_df["APPLICATION_START_DATE"] = bp_df["APPLICATION_START_DATE"].apply(date_clean)
    bp_df = bp_df.drop(bp_df[bp_df.APPLICATION_START_DATE == "rm"].index)

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
    city_columns = bp_df["APPLICATION_START_DATE"].unique().astype(str)
    clean_df = pd.DataFrame(0.0, index = row_series, columns = city_columns)

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
    
    return clean_df 

# City of Chicago Vacant and Abandoned Building Violations

def city_vacant_import_raw():
    city_vacant_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Vacant_and_Abandoned_Buildings_-_Violations_20240217.csv"
    vacant_df = pd.read_csv(city_vacant_path)
    return vacant_df

# LCBH Eviction Data ### READY TO GO
    
def eviction_import_raw():
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

    return clean_df


# ANCILLARY Helper Function, used with City Data:

def date_clean(date):
    '''
    Used to remove data outside of the years in question in the census data.
    '''
    date_year = re.search(r"\d{4}", date)
    date = date_year.group(0)
    if date_year:
        date_year_num = int(date)
        if date_year_num < 2005 or date_year_num > 2023:
            date = "rm"
 
    return date

# THIS REQUIRES THE ADDITION OF THE COMMUNITY AREA PATH.
def colswitch_tools():
    df = gpd.read_file(CA_PATH)
    
    name_num_dict = {}

    for index, row in df.iterrows():
        name_num_dict[df["area_num_1"][index]] = df["community"][index]

    row_series = df["community"]

    return name_num_dict, row_series