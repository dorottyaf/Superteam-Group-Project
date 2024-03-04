import pandas as pd
import geopandas as gpd
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint

variables = ["age", "ethnicity", "household", "educ", "gender", "income", "race"]
COLS_TO_DROP = ["NAME", "state", "county", "tract", "population", "period"]
COLS_TO_DROP2 = ["NAME", "state", "county", "population"]
COLS_TO_DROP3 = [
    "area",
    "area_num_1",
    "area_numbe",
    "comarea",
    "comarea_id",
    "perimeter",
    "shape_area",
    "shape_len",
]


# given a variable name, load in corresponding percentage data
def load_data(name: str):
    """
    Function to load in a dataset for a specific variable (age, income, etc.)

    Args:
        name (string): name of variable (age, race, income)

    Returns (pandas dataframe): dataframe of variable data
    """

    csv_name = name + "_percentage_data.csv"
    filename = pathlib.Path(__file__).parent.parent / "data" / "clean_data" / csv_name
    data = pd.read_csv(filename)
    return data


# getting the shape file for community areas in chicago
def get_chi_shape():
    """
    Grabbing the shape file for Chicago community areas.

    Args:
        None

    Returns (GeoPandas DataFrame): shape file as dataframe
    """

    shp_file = "Boundaries - Community Areas (current)"
    shp_file_path = (
        pathlib.Path(__file__).parent.parent
        / "data_analysis"
        / "Location Information"
        / shp_file
    )
    chi_comm = gpd.read_file(shp_file_path)
    chi_comm = chi_comm.to_crs(epsg=32617)
    # mask for only cook county
    return chi_comm


def make_a_plot(df_sub, p1, p2, dem, community_area):
    """
    Given a demographic (white, black, etc.) within a variavble (race, income, etc.), two time periods,
    and a community area, make a plot for the change in that demographic accross the two periods while outlining
    the community area of interest.

    Args:
        df_sub (pandas dataframe): dataframe of cleaned and merged geodata
        p1 (string): first period to look at
        p2 (string): second period to look at
        dem (string): demographic of interest
        community_area (string): community area of interest

    Returns: None, plots are saved to a folder
    """

    period = p1
    df_plot = df_sub[df_sub["period"] == period]
    df_plot = gpd.GeoDataFrame(df_plot)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    df_plot.plot(column=dem, ax=ax1, cmap="RdPu", legend=True)
    plt.style.use("bmh")
    ax1.set_title(
        "Percentage of Population that is "
        + dem.capitalize()
        + " by Community Area for "
        + period,
        fontdict={"fontsize": "15", "fontweight": "3"},
    )

    period = p2
    df_plot = df_sub[df_sub["period"] == period]
    df_plot = gpd.GeoDataFrame(df_plot)
    df_plot.plot(column=dem, ax=ax2, cmap="RdPu", legend=True)
    comm_area = df_plot[df_plot["community"] == community_area]
    comm_area.plot(ax=ax1, color="none", edgecolor="blue", linewidth=2)
    comm_area.plot(ax=ax2, color="none", edgecolor="blue", linewidth=2)
    plt.style.use("bmh")
    ax2.set_title(
        "Percentage of Population that is "
        + dem.capitalize()
        + " by Community Area for "
        + period,
        fontdict={"fontsize": "15", "fontweight": "3"},
    )
    ax1.axis("off")
    ax2.axis("off")
    png_name = community_area + "_" + dem + "_" + p1 + "_" + p2 + ".png"
    direc = pathlib.Path(__file__).parent / "finished_graphs" / png_name
    plt.savefig(direc)


def given_values_make_plot(variable, per1, per2, community_area):
    """
    This function starts the entire visualizaiton process. It takes a variable of
    interest (race, income, etc.), two time periods, and a community area to make a set of plots
    for each demographic within that variable accross the two time periods.

    Args:
        variable (string): age, income, race, etc.
        per1 (string): first period of interest
        per2 (string): second period of interest
        community_area (string): community area of interest

    Returns: None, plots end up in a folder
    """
    # get cook shape file
    chi_comm = get_chi_shape()

    # pick a variable and load in the data
    df = load_data(variable)

    # cleaning up columns, changing column name for matching
    df = df.drop(columns=COLS_TO_DROP2)
    df = df.rename(columns={"community_area": "community"})

    # merging on column, cleaning up extra columns once again
    df_merge = df.merge(chi_comm, on="community", how="left")
    df_sub = df_merge.drop(columns=COLS_TO_DROP3)
    print(df_sub.columns)

    # making the plots
    for col in df_sub.columns:
        if col != "community" and col != "geometry" and col != "period":
            make_a_plot(df_sub, per1, per2, col, community_area)
