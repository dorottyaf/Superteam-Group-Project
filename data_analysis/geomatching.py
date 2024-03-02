import geopandas as gpd
import pathlib
from collections import namedtuple

'''
Takes inputs based on the datasets people want to use. Options include 3 sets of 
Census tracts by decade (2000, 2010, 2020) and Zip Codes for Chicago for smaller
shapes being rolled up, and Community Area as the larger shape being rolled into.
'''

#Path Variables for shapefiles
PATH_2000 = pathlib.Path(__file__).parent / "Location Information" / "Boundaries - Census Tracts - 2000" / "geo_export_c39c40c3-f0d6-44b1-b60d-c608f5f21ffe.shp" 
PATH_2010 = pathlib.Path(__file__).parent / "Location Information" / "tl_2010_17_tract" / "tl_2018_17_tract.shp"
PATH_2020 = pathlib.Path(__file__).parent / "Location Information" / "tl_2020_17_tract" / "tl_2020_17_tract.shp"
PATH_ZIP = pathlib.Path(__file__).parent / "Location Information" / "Boundaries - ZIP Codes" / "geo_export_0ee546b2-a3fb-4bdb-8cc1-febaad94a4d8.shp"

COMM_AREAS = pathlib.Path(__file__).parent / "Location Information" / "Boundaries - Community Areas (current)" / "geo_export_8fac6090-b29a-4cf4-b6ab-c66b0d4da44a.shp" 

#Name, Path Tuples used to run shape_matcher
TRACT_2000 = ("census_tra", PATH_2000,) 
TRACT_2010 = ("TRACTCE", PATH_2010,)
TRACT_2020 = ("TRACTCE", PATH_2020,)
ZIP_CODES =  ("zip", PATH_ZIP,)


def shape_matcher(small_name, large_name):
    '''
    Inputs: 
        small_name: name of smaller set of shapes, a tuple w/ column name and
            the path variable.
        large_name: name of larger set of shapes- should be COMM_AREAS always
            currently, but set up to allow other large areas if needed.
    
    Example call: shape_dict = shape_matcher(TRACT_2010, COMM_AREAS)

    Returns:
        comm_area_dict: Dictionary where keys are the larger shape, and each value is
        a list of smaller shapes that will be included in 
    '''
    small_df = gpd.read_file(small_name[1])
    large_df = gpd.read_file(large_name)
    large_df = large_df.to_crs(3857)
    small_df = small_df.to_crs(3857)

    comm_area_dict = {}
    for row in large_df.itertuples():
        #Specific to Community Areas, would need to be updated for other maps.
        comm_area_dict[row[6]] = []
    
    small_areas = small_df.area

    for small_ind in small_df.index:
        intersections = large_df.intersection(small_df["geometry"][small_ind])
        intersection_areas = intersections.area
        for large_ind in large_df.index:
            if intersection_areas[large_ind] > (small_areas[small_ind] / 2):
                comm_area_dict[large_df["community"][large_ind]].append(
                    small_df[small_name[0]][small_ind])
                break

    return comm_area_dict

print(shape_matcher(TRACT_2000, COMM_AREAS))