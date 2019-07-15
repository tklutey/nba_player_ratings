# ![pageres](media/logo.jpg)

# Overview

This program provides the offensive rating and defensive rating for each player in each game from the 2018 Playoffs. 

## Design

The implementation is broken into two main steps:
1) Backfill
2) Calculate ratings

### Backfill
The raw data, as provided, is not sufficient to determine player ratings and must be transformed into a more useful form. To do so, we "backfill" three tables (which are in CSV format) that are transformations of the source data.

The three tables are:
1) Canonical Events

*Calculates a "Canonical Game Event Number" for each event in the game, based on the Period(ascending), PC_Time(descending), WC_Time(ascending), Event_Num(ascending)*

2) Lineups

*Provides the 5 players on the floor for a given rotation (i.e. 5 players and the starting canonical game event number and the ending canonical game event number of that rotation*)

3) Matchups

*For a given gameID, joins them with the two teamIds of the teams involved*

### Calculate

There are 5 game events that can impact a player's offensive and defensive rating:
1) Made FG
2) Missed FG
3) Turnover
4) End of period
5) Free throw

For each of these events, we query the Lineups table for the players on the floor and adjust their ratings accordingly. Additional logic is necessary for free throws, where the lineup on the floor at the time of the free throw may not be the same as that that should be scored.
# Usage

## Install

### Prerequisites
To work with this repo, you must have Conda installed. Conda is a command line tool to manage dependencies within a virtual environment.

### Steps
1) From the project root directory, run:
```
conda env create -f environment.yml
```
This creates a conda environment with all of the necessary dependencies to run this package.


2) Run ```source activate [environment_name]``` on OSX or simply ```activate [environment_name]``` on Windows to activate the conda virtual environment.

**Note: see https://conda.io/docs/user-guide/tasks/manage-environments.html for more information on managing Conda environments**

## Build Targets

You can run this project from the root with the following command:

```make all```

The output will be in <root>/data/output/csv/Ratings.csv.

To run *only* the backfill part of the program, run:

```make backfill```

To run all unit tests and codestyle, run:

```make release```