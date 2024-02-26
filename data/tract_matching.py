from data_analysis.geomatching import TRACT_2000, TRACT_2010, TRACT_2020, \
   COMM_AREAS, shape_matcher
import pathlib
import pandas as pd

tracts_2000 = shape_matcher(TRACT_2000, COMM_AREAS)
tracts_2010 = shape_matcher(TRACT_2010, COMM_AREAS)
tracts_2020 = shape_matcher(TRACT_2020, COMM_AREAS)

TRACT_TO_PERIOD = {"2005-2009" : tracts_2000, "2010-2014": tracts_2010, \
                   "2015-2019" : tracts_2010, "2018-2022" : tracts_2020}


def clean_tract_names(tracts: dict):
   """
   Takes a dictionary mapping community areas to tracts and removes any 
   leading zeroes from the tract code to match the census data
   """
   AREAS_WITH_ZERO = ["LINCOLN SQUARE", "ROGERS PARK", "WEST RIDGE", "UPTOWN", \
                      "NEAR NORTH SIDE", "LAKE VIEW", "NORTH CENTER", \
                      "LINCOLN PARK", "EDGEWATER", "EDISON PARK"]

   for community, tract in tracts.items():
      if community in AREAS_WITH_ZERO:
         for i, instance in enumerate(tract):
            if instance[0] == "0":
               tract[i] = instance[1:]
   
   return tracts


def custom_agg(series: pd):
   """
   Builds a helper function for the aggregate pandas feature so that if the 
   column in pandas is numeric, then upon merging the rows the function takes
   the sum, and if it's a string, it takes the first string instance and applies
   that string for the rest of the merge
   """
   if pd.api.types.is_numeric_dtype(series):
      return series.sum()
   elif pd.api.types.is_object_dtype(series):
      return series.iloc[0]
   else:
      return None


def tract_to_community(dataset:pd, tract_dictionary:dict):
   """
   Takes a dataset and combines the tracts into the community areas for 
   that year
   """
   # setting tract, state, and county columns to strings
   # tract needs to be a string to be comparable with the dictionary
   # the other two need to be strings so they're aggregated as strings not ints
   dataset["tract"] = dataset["tract"].astype(str)
   dataset["state"] = dataset["state"].astype(str)
   dataset["county"] = dataset["county"].astype(str)

   # replace tract names with their community area names and combine rows with 
   # the same community area name
   for community, tracts in tract_dictionary.items():
      for tract in tracts:
         dataset.replace({"tract": {tract : community}}, inplace = True)
   dataset = dataset.groupby("tract").agg(custom_agg).reset_index()
    
   return dataset


def drop_suburbs(dataset: pd):
   """
   Drop all the tracts which were not mapped to a community area as they are
   tracts in Cook County which are outside the bounds of the city of Chicago
   """

   sorted_data = dataset.sort_values("tract")
   chicago_data = sorted_data[-77:]
   chicago_data = chicago_data.rename(columns = {"tract" : "community_area"})

   return chicago_data


def get_community_areas(dataset:pd, period:str):
   """
   Takes a pandas dataframe and maps the tracts to community areas in Chicago.
   If a tract is outside of Chicago, it drops it
   """
   tracts = TRACT_TO_PERIOD[period]
   tract_dictionary = clean_tract_names(tracts)

   community_dataset = tract_to_community(dataset, tract_dictionary)
   without_suburbs = drop_suburbs(community_dataset)

   return without_suburbs
