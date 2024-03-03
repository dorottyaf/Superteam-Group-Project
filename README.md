# Change in Chicago: Analysis and Visualizations (CAPP 30122 Winter 2024)
## Echo Nattinger, Paul Soltys, Dorka Frisch, and Andrew Baker

This project studies demographic change in Chicago community areas in relationship with fluctuations in the housing and economic markets. Specifically, the goal of this project was to study the biggest demographic shifts in Chicago and study potential causes behind those changes. To this end, we gathered demographic data using the United States Census American Community Survey (ACS) API and housing/economic data from a number of secondary sources, including the DePaul Housing Institute, the City of Chicago, and the Law Center for Better Housing. 

Using a fuzzy geomatching algorithm, we grouped our tract-level Census data into community area data. When run as an app, this project allows a user to study the biggest demographic shifts out of all Chicago neighborhoods, visualize these changes, and investigate contemperaneous change in housing or economic measurements. 

To run this project on your own machine, complete the following steps: 

Note: This project requires poetry to be installed 

1) Ensure [poetry is installed on your local machine](https://python-poetry.org/docs/)

2) Clone the repository onto your own machine using `git clone git@github.com:dorottyaf/Superteam-Group-Project.git` (SSH) or `git clone https://github.com/dorottyaf/Superteam-Group-Project.git` (HTTPS)

3) Run `poetry shell`

4) Run `poetry install`

5) To initiate the app, run `py -m chicago_demographic_change`

6) Follow the prompts given to you by the app. Explore the change in Chicago demographics, investigate local changes in housing markets, and visualize to your heart's content!

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._
