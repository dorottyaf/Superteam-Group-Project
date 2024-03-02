import pathlib
import pandas as pd
import json
import re


# Note that most of these datasets have year limitations tighter than ACS Data
# Business License and Building Permit groupings cut down locally to shareable
# csvs of counts, have 1.1m and 750k records respectively

# DePaul Housing Institute Pricing Index
# UnConverted .xls file for if people need contextual information from the data
def depaul_import_raw():
    depaul_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
    df = pd.read_csv(depaul_path)
    return df

### City of Chicago Business License Counts ###

def city_blc_clean():
    ''' Outputs a dictionary with not ideal keys, but year/community area counts of 
    business license applications. Not sure if the data in the early years is any good.
    '''
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
    permit_df = pd.read_csv(city_permit_path)

    permit_df["APPLICATION_START_DATE"] = permit_df["APPLICATION_START_DATE"].astype(str)
    permit_df["APPLICATION_START_DATE"] = permit_df["APPLICATION_START_DATE"].apply(date_clean)
    permit_df = permit_df.drop(permit_df[permit_df.APPLICATION_START_DATE == "rm"].index)

    data_years = set(permit_df["APPLICATION_START_DATE"])
    counts_dict = {}

    for year in data_years:
        year_df = permit_df[permit_df["APPLICATION_START_DATE"] == year]
        area_counts = year_df["COMMUNITY_AREA"].value_counts()
        for area in area_counts.index:
            key = str(year + ", " + str(area))
            counts_dict[key] = area_counts[area]

    # need to add proper filepath
    with open("raw_data\Secondary Data\permit_clean.json", "w") as readout:
        json.dump(counts_dict, readout)

    return counts_dict #Need to print to a csv somewhere, perhaps.

def city_permit_import_raw():
    '''DATA FILE FOR THIS HAS NOT BEEN UPLOADED.'''
    city_permit_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Building_Permits_20240217.csv"
    permit_df = pd.read_csv(city_permit_path)
    return permit_df

# City of Chicago Vacant and Abandoned Building Violations

def city_vacant_import_raw():
    city_vacant_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "Vacant_and_Abandoned_Buildings_-_Violations_20240217.csv"
    vacant_df = pd.read_csv(city_vacant_path)
    return vacant_df

# LCBH Eviction Data
    
def eviction_import_raw():
    eviction_path = pathlib.Path(__file__).parent / "raw_data" / "Secondary Data" / "eviction_data_comm_area.csv"
    df = pd.read_csv(eviction_path)
    return df


# ANCILLARY Helper Function:

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

test_dict = city_blc_clean()
test_dict2 = city_permit_clean()