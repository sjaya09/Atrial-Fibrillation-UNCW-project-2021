"""
Georgia Smith
2021 Senior Capstone Project

extract_age_variables.py

This is the first script run

It isolates the age variables from the ncsr dataset and saves it as a csv
"""

import pandas as pd
import numpy as np
from ncsr_import import ncsr_data
import copy


# Pull ncsr data from file ncsr_import
ncsr = ncsr_data()
  # ncsr.ncsr holds all of the data from NCS 20240
  # https://www.icpsr.umich.edu/web/ICPSR/studies/20240
  # Alegria, Margarita, Jackson, James S. (James Sidney), Kessler, Ronald C., and Takeuchi, David. Collaborative Psychiatric Epidemiology Surveys (CPES), 2001-2003 [United States]. Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor], 2016-03-23. https://doi.org/10.3886/ICPSR20240.v8
  # Key Functions:
    # ncsr.search_for_description looks for a descriotion of a column name in ncs1.dxdm or ncs1.survey
    # ncsr.get_variable_info queries icpsr for information like values, variable descriptions, and more
    # ncsr.get_value_from_string takes in a string that is a var name of dataframe in the ncsr description tree. Tree can be traversed using ncsr.root
  # Key Variables:
    # ncsr.ncsr 
    # ncsr.tree (Tree including descriptions of survey and dxdm columns)
    # ncsr.root (root used in traversing ncsr.tree)



# below code is used to isolate variables that have do do with onset age of symptoms
age_variable_subset = pd.DataFrame(columns = ['VarName', 'Description', 'Root_DF', 'Start', 'End', 'DataFrame', 'recursion_flag'])


for x in range(1, len(ncsr.root)):
    age_variable_subset = age_variable_subset.append(
        ncsr.get_value_from_string(ncsr.root.iloc[x,0])[
            np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*.*", False)) & np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*(^Age |^Age| age )+.*", False)) & np.logical_not(np.array(ncsr.get_value_from_string(ncsr.root.iloc[x,0])['Description'].str.match(".*(^Remember|^Exact|^Age$|#|biological|when you were born|^Freq)+.*", False)))
            ]
    )

age_variable_subset = age_variable_subset.reset_index(drop=True)
   #reset index to bc the appending gives repeating index values which leads to confustion

#age_variable_subset.to_csv('age_variable_with_descriptions.csv')
    #^ uncomment to save age variables w/ descriptions to csv



ncsr_age_vars = ncsr.ncsr[list(age_variable_subset.iloc[:, 0])]
    # Grab only the variables in ncsr.ncsr found w/ age_variable_subset

for y in range(0, len(ncsr_age_vars)):
    #initialize the age values taking out NaN values and Subject did not answer values and setting them to -1
    current_case = y
    case_age_vars = []
    for val, x in enumerate(age_variable_subset.iloc[:, 0]): 
            if ncsr_age_vars.loc[y, x] != ' ':
                if ncsr_age_vars.loc[y, x] != '.' and int(ncsr_age_vars.loc[y,x]) > 1 and int(ncsr_age_vars.loc[y,x]) < 100:
                    # Note subject age range is 18 - 99 so there should be no values above 100
                    ncsr_age_vars.loc[y, x] = int(ncsr_age_vars.loc[y,x])
                else: 
                    ncsr_age_vars.loc[y, x] = 0
            else:
                ncsr_age_vars.loc[y,x] = 0


ncsr_age_vars.to_csv('justage_vars_init.csv')
  #^uncomment to save age variable subset of ncsr as csv


