import pandas as pd
import geopandas as gpd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint

variables = ["age", "ethnicity", "household", "educ", "gender", "income", "race"]
COLS_TO_DROP = ['NAME', 'state', 'county', 'tract', 'population', 'period']
COLS_TO_DROP2 = ['NAME', 'state', 'county', 'population']
COLS_TO_DROP3 = ['area', 'area_num_1', 'area_numbe', 'comarea', 'comarea_id', 'perimeter', 'shape_area', 'shape_len']

# given a variable name, load in corresponding percentage data
def load_data(name:str):
    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / csv_name
    data = pd.read_csv(filename)
    return data

# getting the shape file for community areas in chicago
def get_chi_shape():
    shp_file = "Boundaries - Community Areas (current)"
    shp_file_path = pathlib.Path(__file__).parent.parent / "data_analysis" / 'Location Information' / shp_file
    chi_comm = gpd.read_file(shp_file_path)
    chi_comm = chi_comm.to_crs(epsg = 32617)
    # mask for only cook county
    return chi_comm

def make_a_plot(df_sub, p1, p2, dem, community_area):
    period = p1
    df_plot = df_sub[df_sub['period'] == period]
    df_plot = gpd.GeoDataFrame(df_plot)
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize = (20, 10))
    df_plot.plot(column = dem,
                ax = ax1,
                cmap = "RdPu",
                legend = True)
    plt.style.use('bmh')
    ax1.set_title('Percentage of Population that is ' + dem.capitalize() + ' by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})

    period = p2
    df_plot = df_sub[df_sub['period'] == period]
    df_plot = gpd.GeoDataFrame(df_plot)
    df_plot.plot(column = dem,
                ax = ax2,
                cmap = "RdPu",
                legend = True)
    comm_area = df_plot[df_plot['community'] == community_area]
    comm_area.plot(ax = ax1, color='none', edgecolor= 'blue', linewidth = 2)
    comm_area.plot(ax = ax2, color='none', edgecolor= 'blue', linewidth = 2)
    plt.style.use('bmh')
    ax2.set_title('Percentage of Population that is ' + dem.capitalize() + ' by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})
    ax1.axis('off')
    ax2.axis('off')
    png_name = community_area + '_' + dem + '_' + p1 + '_' + p2 + '.png'
    direc = pathlib.Path(__file__).parent / 'finished_graphs' / png_name
    plt.savefig(direc)
    




def given_values_make_plot(variable, per1, per2, community_area):
    #get cook shape file
    chi_comm = get_chi_shape()

    # pick a variable and load in the data
    df = load_data(variable)

    # cleaning up columns, changing column name for matching
    df = df.drop(columns= COLS_TO_DROP2)
    df = df.rename(columns={'community_area' : 'community'})

    # merging on column, cleaning up extra columns once again
    df_merge = df.merge(chi_comm, on= 'community', how= 'left')
    df_sub = df_merge.drop(columns= COLS_TO_DROP3)
    print(df_sub.columns)

    # making the plots
    for col in df_sub.columns:
        if col != 'community' and col != 'geometry' and col != 'period':
            make_a_plot(df_sub, per1, per2, col, community_area)

def run():
    # ask the user what they want to see
    variable = input('What variable ("age", "ethnicity", "household", "educ", "gender", "income", "race") would you like to see?')
    per1 = input('What period (2005-2009, 2010-2014, 2015-2019, 2018-2022) would you like to start with?')
    per2 = input('What period (2005-2009, 2010-2014, 2015-2019, 2018-2022) would you like to end with?')
    community_area = input('What community area would you like to see this on? (ALL CAPS PLEASE)')


    given_values_make_plot(variable, per1, per2, community_area)





'''
make_a_plot(df_sub, '2005-2009', '2010-2014', "black")
make_a_plot(df_sub, '2005-2009', '2010-2014', "white")
'''




























"""
period = '2005-2009'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
fig, (ax1,ax2) = plt.subplots(1, 2, figsize = (20, 10))
df_plot.plot(column = "white",
                ax = ax1,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax1.set_title('Percentage of Population that is White by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})
# plt.show()


period = '2010-2014'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
# fig, ax = plt.subplots(1, 1, figsize = (20, 10))
df_plot.plot(column = "white",
                ax = ax2,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax2.set_title('Percentage of Population that is White by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})
plt.show()



period = '2005-2009'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
fig, (ax1,ax2) = plt.subplots(1, 2, figsize = (20, 10))
df_plot.plot(column = "black",
                ax = ax1,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax1.set_title('Percentage of Population that is Black by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})
# plt.show()


period = '2010-2014'
df_plot = df_sub[df_sub['period'] == period]
df_plot = gpd.GeoDataFrame(df_plot)
print(df_plot)

# Create subplots
# fig, ax = plt.subplots(1, 1, figsize = (20, 10))
df_plot.plot(column = "black",
                ax = ax2,
                cmap = "RdPu",
                legend = True)
# Stylize plots
plt.style.use('bmh')

# Set title
ax2.set_title('Percentage of Population that is Black by Community Area for ' + period, fontdict = {'fontsize': '15', 'fontweight' : '3'})
plt.show()
plt.clf()
"""












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