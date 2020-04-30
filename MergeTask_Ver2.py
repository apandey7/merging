# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:59:09 2020

@author: u325180
"""
"""
Description:
    This code will seperately create 3 DataFrames for each file: Global access, CountryWise access 
    and Region Mapping.
"""
import pandas as pd
import numpy as np

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
lst_output_cols = ["Country","Segment","IDs"]
df_output = pd.DataFrame(columns = lst_output_cols)

#Setting up the output table
#Filling all unique countries and all segments in front of it

max_segments = max(len(df_regional["Segment"].unique()),len(df_country["Segment"].unique()), len(df_global["Segment"].unique()))
df_output["Country"] = pd.concat([df_region_map["Country"]]*(max_segments-1) , ignore_index=True)
unique_countr = len(df_output["Country"].unique())

df_seg = pd.DataFrame(columns=["Segment"])
df_seg = pd.Series(df_country["Segment"].unique())
df_seg = df_seg[:-1]
df_seg.columns = ["Segment"]

df_output["Segment"] = pd.concat([df_seg]*unique_countr, ignore_index=True)

lst_global_Ids = []
for i in df_global.values:
    print(i)
    lst_global_Ids.append(i)
#
lst_global_ToStr = ';'.join(map(str, lst_global_Ids))
df_output["IDs"] = lst_global_ToStr




#Country Mapping DataFrame
#df_country.groupby(["ClientID","Segment"])["Country"].sum().reset_index()
df_tmp = df_country[['ClientID','Country','Segment']]
#df_output_ctry = pd.DataFrame(columns = lst_output_cols)
df_tmp = df_tmp.groupby(['Country','Segment'])["ClientID"]
df_output_temp = df_output.groupby(['Country','Segment'])
for key,values in df_tmp:
#    print(key)
    for k,v in df_output_temp:
#        print(k)
        if(key==k):
#            print(key)
#            print("hello")
#            print(v)
            y = v["IDs"] + ";" +str(values.to_string(index=False))
            df_output.loc[y.index,'IDs'] = y



df_temp_regional = (df_regional[['ID','Segment','Region']].merge(df_region_map, how='left'))


#Country Mapping DataFrame
#df_country.groupby(["ClientID","Segment"])["Country"].sum().reset_index()
df_tmp_1 = df_temp_regional[['ID','Country','Segment']]
#df_output_ctry = pd.DataFrame(columns = lst_output_cols)
df_tmp_1 = df_tmp_1.groupby(['Country','Segment'])["ID"]

df_output_temp = df_output.groupby(['Country','Segment'])

for key,values in df_tmp_1:
#    print(key)
    for k,v in df_output_temp:
#        print(k)
        if(key==k):
#            print(key)
#            print("hello")
#            print(v)
            y = v["IDs"] + ";" +str(values.to_string(index=False))
            df_output.loc[y.index,'IDs'] = y


df_output


#Concatenating the three dataFrames created above
df_output = pd.concat([df_output_global, df_output_ctry, df_output_regn], axis=0)

#This output df_output is the dataframe to be sent to excel as output
