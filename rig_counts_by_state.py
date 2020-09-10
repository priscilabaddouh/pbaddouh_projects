# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:57:26 2020
Baker Hughes Rig Count:
Rig Count
https://rigcount.bakerhughes.com/na-rig-count

@author: pbaddouh

Original paths were removed from this sample code.
"""

import urllib.request, urllib.parse, urllib.error
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import xlrd

#Add the path
path='...'

#Scraping all files from the website
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

url = "https://rigcount.bakerhughes.com/na-rig-count"
headers={'User-Agent':user_agent,} 

request=urllib.request.Request(url,None,headers) 
html = urllib.request.urlopen(request)

soup = BeautifulSoup(html, 'html.parser')
tb=soup.find('tbody')

names=list()
urls=list()
tags=tb('a')
for tag in tags:
    if tag.has_attr('href'):
        url=tag['href']
        urls.append(url)
        headers={'User-Agent':user_agent,}

        #Add path
        path='...'
        name=str(tag['title'])
        filename=path+name
        r=requests.get(url,allow_redirects=True)
        if re.findall('^Rigs by State_',str(tag['title'])) and re.findall('xlsx',str(tag['title'])):
            #renaming the file tha we will be using
            filename2=path+'Rigs by State Most Current.xlsx'
            open(filename2,'wb').write(r.content)
        else:
            open(filename,'wb').write(r.content)

#Getting all of the tabs in the spreadsheet that we need into a list
file='.../Rigs by State Most Current.xlsx'
xls=xlrd.open_workbook(file,on_demand=True)
sheet_n=xls.sheet_names()

#Getting each, transposing it, deleting blank columns and creating the data frame.
rig_df = pd.DataFrame() 
for tab in sheet_n:
    xls2=pd.ExcelFile(file)
    df=xls2.parse(tab,skiprows=3,parse_cols="A:J",header=1,skipfooter=1)
    #Dropping blank columns
    df.rename({'Unnamed: 2':'a','Unnamed: 4':'b','Unnamed: 6':'c','Unnamed: 8':'d','Unnamed: 10':'e','Unnamed: 12':'f'},axis="columns",inplace=True)
    df.drop(['a','b','c','d','e'], axis=1, inplace=True)
    df=df.transpose().reset_index().rename(columns={'index':'Date'})
    headers=df.iloc[0].str.strip()
    df=pd.DataFrame(df.values[1:], columns=headers)
    df.rename(columns={'Unnamed: 0':'Date'},inplace=True)
    df=df.loc[:,df.columns.notnull()] # delete columns that have only nulls
    df['Year']=int('20'+str(tab[-2:])) # creating a variable for year
    #Dropping values equal to f, this is from the unnamed from tabs that have more than 4 weeks in a month
    df=df[df.Date !='f']
    rig_df = rig_df.append(df)

x=rig_df['Year']
rig_df.drop(labels=['Year'],axis=1,inplace=True)
rig_df.insert(1,'Year',x)
print(rig_df)

#Creating a data frame with totals
df_totals=rig_df.filter(regex='Date|Year|TOTAL')

parent = os.path.normpath(os.getcwd())
rig_df.to_csv(os.path.join(parent, os.path.join('Output', 'rig_count.csv')), index=False)
df_totals.to_csv(os.path.join(parent, os.path.join('Output', 'rig__total_counts.csv')), index=False)
