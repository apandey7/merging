# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:58:52 2020

@author: Ankit Pandey
"""

"""
Description:
    This code will seperately create 3 DataFrames for each file: Global access, CountryWise access 
    and Region Mapping.
"""
import pandas as pd

#Reading all the sheets as different DataFrames
df_global = pd.read_excel("D:\\AP\\task\\Input.xlsx", sheet_name="Global")
df_regional = pd.read_excel("D:\\AP\\task\\Input.xlsx", sheet_name="Regional")
df_country = pd.read_excel("D:\\AP\\task\\Input.xlsx", sheet_name="Country")
df_region_map = pd.read_excel("D:\\AP\\task\\Input.xlsx", sheet_name="Region-Country mapping")

#Checking out the rows X columns in each dataframes
df_global.shape
df_regional.shape
df_country.shape
df_region_map.shape

#Creating a list of output columns required: This lit will be called out for each DataFrame
lst_output_cols = ["ID","Segment","Countries"]
df_output = pd.DataFrame(columns = lst_output_cols)


#Global entry DataFrame
df_output_global = pd.DataFrame(columns = lst_output_cols)
df_output_global["ID"] =  df_global["ID"]
df_output_global["Segment"] =  df_global["Segment"]
df_output_global["Countries"] =  "All"


#Country Mapping DataFrame
#df_country.groupby(["ClientID","Segment"])["Country"].sum().reset_index()
df_tmp = df_country.groupby(["ClientID","Segment"])
df_output_ctry = pd.DataFrame(columns = lst_output_cols)
for state, frame in df_tmp:
    #print(state[0])
    lst_ctry = list(frame["Country"])
#    Below code changes list to string with ; as seperator
    listToStr = ';'.join(map(str, lst_ctry))
    data = [{"ID" : state[0], "Segment": state[1], "Countries": listToStr}]
    df_output_ctry = df_output_ctry.append(data)


#Regional Mapping DataFrame
#df_regional
#df_region_map
df_output_regn = pd.DataFrame(columns = lst_output_cols)
for items in df_regional.values:
    lst_ctry_rgn = []
#    print(items)
#    print("ID",items[0])
    for key,value in df_region_map.values:
        if(key == items[1]):
            lst_ctry_rgn.append(value)
#    Below code changes list to string with ; as seperator
    listToStr = ';'.join(map(str, lst_ctry_rgn))
    data = [{"ID" : items[0], "Segment": items[2], "Countries": listToStr}]
    df_output_regn = df_output_regn.append(data)




#Concatenating the three dataFrames created above
df_output = pd.concat([df_output_global, df_output_ctry, df_output_regn], axis=0)

#This output df_output is the dataframe to be sent to excel as output
