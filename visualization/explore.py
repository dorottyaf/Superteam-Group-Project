import pandas as pd
import geopandas as gpd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from data_analysis.geomatching import TRACT_2000, TRACT_2010, TRACT_2020, \
   COMM_AREAS, shape_matcher
import pprint

variables = ["age", "ethnicity", "household", "educ", "gender", "income", "race"]
COLS_TO_DROP = ['NAME', 'state', 'county', 'tract', 'population', 'period']
COLS_TO_DROP2 = ['NAME', 'state', 'county', 'tract', 'population']
COLS_TO_DROP3 = ['COUNTYFP', 'NAME', 'NAMELSAD', 'MTFCC', 'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON']
age_top_10 = [835700, 611800, 834600, 670100, 251700, 835600, 690500, 380500, 830201, 841400]
eth_top_10 = [611700, 243000, 310400, 841600, 240800, 230600, 843400, 220400, 832400, 10702]
hh_top_10 = []
educ_top_10 = []
gender_top_10 = []
inc_top_10 = []
race_top_10 = []

def load_data(name:str):
    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / "tract_based" /  csv_name
    data = pd.read_csv(filename)
    return data


def get_cook_shape():
    shp_file = "tl_rd22_17_tract.zip"
    shp_file_path = pathlib.Path(__file__).parent / "shapes" / shp_file
    il_tract = gpd.read_file(shp_file_path)
    il_tract = il_tract.to_crs(epsg = 32617)
    mask = il_tract['COUNTYFP'] == '031'
    cook_tract = il_tract[mask]
    return cook_tract

'''
# for exporatory, getting tracts with greatest changes for each of 7 variables
for var in variables:
    df = load_data(var)
    group = df.groupby("tract")
    if var == "age":
        for name, data in group:
            if name in age_top_10:
                for time in set(data['period']):
                    data_by_time = data[data['period'] == time]
                    data_by_time = data_by_time.drop(columns = COLS_TO_DROP)
                    data_by_time_t = data_by_time.transpose()
                    plt.plot(data_by_time_t.index, data_by_time_t.values, marker='o', linestyle='-', label = time)
                plt.xlabel('Age Range')
                plt.ylabel('Percentage of Population in Age Range')
                plt.title("Changes in Age Distribution Over Time for Tract: " + str(name))
                plt.legend()
                png_name = str(name) + "_age_plot.png"
                direc = pathlib.Path(__file__).parent / 'temp_graphs' / png_name
                plt.savefig(direc)
                plt.clf()
    if var == "ethnicity":
        for name, data in group:
            if name in eth_top_10:
                for time in set(data['period']):
                    data_by_time = data[data['period'] == time]
                    data_by_time = data_by_time.drop(columns = COLS_TO_DROP)
                    data_by_time_t = data_by_time.transpose()
                    plt.plot(data_by_time_t.index, data_by_time_t.values, marker='o', linestyle='-', label = time)
                plt.xlabel('Ethnicity')
                plt.ylabel('Percentage of Population of Ethnicity')
                plt.title("Changes in Ethnicity Distribution Over Time for Tract: " + str(name))
                plt.legend()
                png_name = str(name) + "_ethnicity_plot.png"
                direc = pathlib.Path(__file__).parent / 'temp_graphs' / png_name
                plt.savefig(direc)
                plt.clf()
                '''


cook_tract = get_cook_shape()
comm_dict = shape_matcher(TRACT_2000, COMM_AREAS)
print(comm_dict)
for var in variables:
    df = load_data(var)
    df["GEOID"] = df['state'].astype(str) + '0' + df['county'].astype(str) + df['tract'].astype(str)
    df = df.drop(columns= COLS_TO_DROP2)
    df_merge = df.merge(cook_tract, on= 'GEOID', how= 'left')
    df_sub = df_merge.drop(columns= COLS_TO_DROP3)
    # doing just one period
    df_sub = df_sub[df_sub['period'] == '2005-2009']
    df_sub = gpd.GeoDataFrame(df_sub)
    if var == 'race':
        print(cook_tract.head(2))
        print('Shape, ', cook_tract.shape)
        print("\nThe shapefile projection is: {}".format(cook_tract.crs))
        print(df)
        print(df_merge)
        print(df_sub)
        print(df_sub.columns)
        # Create subplots
        fig, ax = plt.subplots(1, 1, figsize = (20, 10))
        df_sub.plot(column = "white",
                       ax = ax,
                       cmap = "RdPu",
                       legend = True)
        # Stylize plots
        plt.style.use('bmh')

        # Set title
        ax.set_title('Percentage of Population that is White by Tract for 2005-2009', fontdict = {'fontsize': '25', 'fontweight' : '3'})
        plt.show()
        plt.clf()
