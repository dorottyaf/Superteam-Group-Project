import geopandas as gpd
import pathlib
from collections import namedtuple

def tract_import_raw():
    tract_path = pathlib.Path(__file__).parent / "Location Information" / "tl_2010_17001_tract00" / "tl_2010_17001_tract00.shp"
    tracts_df = gpd.read_file(tract_path)
    return tracts_df

def comm_area_import_raw():
    ca_path = pathlib.Path(__file__).parent / "Location Information" / "Boundaries - Community Areas (current)" / "geo_export_8fac6090-b29a-4cf4-b6ab-c66b0d4da44a.shp"
    ca_df = gpd.read_file(ca_path)
    return ca_df

def zip_import_raw():
    zip_path = pathlib.Path(__file__).parent / "Location Information" / "Boundaries - ZIP Codes" / "geo_export_0ee546b2-a3fb-4bdb-8cc1-febaad94a4d8.shp"
    zip_df = gpd.read_file(zip_path)
    return zip_df

# Goal - 2 Dictionaries, one mapping census tract -> comm area, one zip -> comm area

def geodict_generator(data_frame):
    
    comm_area_dict = {}
    for row in data_frame.itertuples():
        comm_area_dict[row[6]] = []
    
    return comm_area_dict

def shape_matcher(small_df, large_df):

    large_df = large_df.to_crs(3857)
    small_df = small_df.to_crs(3857)
    comm_area_dict = geodict_generator(large_df)
    
    small_areas = small_df.area

    for small_ind in small_df.index:
        intersections = large_df.intersection(small_df["geometry"][small_ind])
        intersection_areas = intersections.area
        for large_ind in large_df.index:
            if intersection_areas[large_ind] > (small_areas[small_ind] / 2):
                comm_area_dict[large_df["community"][large_ind]].append(small_df["TRACTCE"][small_ind])
                break

    return comm_area_dict
