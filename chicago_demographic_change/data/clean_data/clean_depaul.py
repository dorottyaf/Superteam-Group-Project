import pathlib
import pandas as pd


YEARS = ["2005-2009", "2010-2014", "2015-2019", "2018-2022"]
NOT_CHICAGO = ["COOK","CHICAGO","SUBURBS","Palatine/Barrington","Melrose Park/Maywood",\
               "Oak Park/Cicero","LaGrange/Burbank","Orland Park/Lemont",\
                "Oak Lawn/Blue Island","Oak Forest/Country Club Hills",\
                "Calumet City/Harvey","Chicago Heights/Park Forest",\
                "Arlington Heights/Wheeling","Winnetka/Northbrook",\
                "Hoffman Estates/Streamwood","Schaumburg","Mount Prospect/Elk Grove Village",\
                "Park Ridge/Des Plaines", "Evanston/Skokie","Elmwood Park/Franklin Park"]
PERIODS = [("2005-2009", "2010-2014"),("2010-2014", "2015-2019"), \
           ("2015-2019", "2018-2022"), ("2005-2009", "2018-2022")]


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

    # calculating change
    for period1, period2 in PERIODS:
        text = period1 + " to " + period2
        change_columns.append(text)
        dataframe[text] = abs(dataframe[period1] - dataframe[period2])

    for column in change_columns:
        mid_bound = dataframe[column].quantile(q = 0.333, interpolation = "lower")
        high_bound = dataframe[column].quantile(q = 0.666, interpolation = "lower")
        lmh_bins = [float("-inf"), mid_bound, high_bound, float("inf")]
        dataframe[column] = pd.cut(dataframe[column], bins = lmh_bins, labels = ["low", "medium", "high"])

    print(dataframe["2010-2014"].value_counts())
    return dataframe


def get_clean_dataframe():
    """
    Does all the necessary cleaning and returns a clean dataframe
    """

    # load depaul file
    filename = pathlib.Path(__file__).parent.parent / "raw_data" / "Secondary Data" / "IHS_DePaul_Index.csv"
    depaul = pd.read_csv(filename)

    depaul = community_fix(depaul)
    depaul = transpose(depaul)
    depaul = delete_irrelevant_years(depaul)
    depaul = combine_years(depaul)
    depaul = get_change_columns(depaul)

    print(depaul)

    filename = pathlib.Path(__file__).parent / "Secondary Data" / "IHS_DePaul_Index.csv"
    depaul.to_csv(filename, index = False)

get_clean_dataframe()