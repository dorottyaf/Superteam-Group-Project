# Change in Chicago: Analysis and Visualizations (CAPP 30122 Winter 2024)
## Echo Nattinger, Paul Soltys, Dorka Frisch, and Andrew Baker

This project studies demographic change in Chicago community areas in relationship with fluctuations in the housing and economic markets. Specifically, the goal of this project was to study the biggest demographic shifts in Chicago and study potential causes behind those changes. To this end, we gathered demographic data using the United States Census American Community Survey (ACS) API and housing/economic data from a number of secondary sources, including the DePaul Housing Institute, the City of Chicago, and the Law Center for Better Housing. 

Using a fuzzy geomatching algorithm, we grouped our tract-level Census data into community area data. When run as an app, this project allows a user to study the biggest demographic shifts out of all Chicago neighborhoods, visualize these changes, and investigate contemperaneous change in housing or economic measurements. 

Note: the following instructions assume you are running the commands from the root Superteam-Group-Project directory

To run this project on your own machine, complete the following steps: 

1) Ensure [poetry is installed on your local machine](https://python-poetry.org/docs/)

2) Clone the repository onto your own machine using `git clone git@github.com:dorottyaf/Superteam-Group-Project.git` (SSH) or `git clone https://github.com/dorottyaf/Superteam-Group-Project.git` (HTTPS)

3) Run `poetry install`

4) Run `poetry shell`

5) To initiate the app, run `py -m chicago_demographic_change`

6) Follow the prompts given to you by the app. You will be asked to input a number, k -- the app will generate the top k changes in Chicago across all years and all variables. You can then further investigate changes by specific demographic variables, visualize these changes, and investigate how a number of economic and housing measures changed alongside demographic changes. Follow the instructions to learn about the ever-changing city of Chicago!

Our app allows you to explore changes in the following demographic variables:

- gender: Male, Female identification
- race: racial identification according to U.S. Census categories
- ethnicity: ethnic identification according to U.S. Census categories
- income: individual income in USD
- household: household income in USD
- age: age in years
- education: highest level of educational attainment

A brief description of secondary data sources available to you in analysis include:

- City Building Permits: Building permit applications submitted - a rough proxy of new or additional construction activity.
- City Business Licenses: Business license applications submitted - a rough proxy of new or additional economic activity.
- Eviction Filings: The number of eviction proceedings filed in an area - conceptually may be linked to higher rents or property values (data available only for 2010-2019).
- DePaul Housing Price Index: an index of home prices relative to the year 2000 - a measure of homeowner costs in an area.
- City Vacant and Abandoned Building Violations: Recorded complaints investigated by the city related to derelict or empty buildings (data available only for 2010-2022). 

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._
