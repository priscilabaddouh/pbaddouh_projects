# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:06:43 2020

@author: pbaddouh

Original data from: https://btc.com/stats/pool?pool_mode=all

Original paths were deleted from this sample code.

"""

import urllib.request, urllib.parse, urllib.error
import pandas as pd
from bs4 import BeautifulSoup
import ssl
import os

#Add path
path='...'

#Getting the data from BTC
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url="https://btc.com/stats/pool?pool_mode=all"
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tb=soup.find('table', class_="table table-hover pool-panel-share-table")

df=pd.DataFrame(columns=range(0,9),index=[0])
btc_table=pd.DataFrame(columns=range(0,9),index=[0])

row_marker=0
for row in tb.find_all('tr'):
    column_marker=0
    columns=row.find_all('td')
    for column in columns:
        df.iat[row_marker,column_marker]=column.get_text().strip()
        column_marker+=1
    btc_table=btc_table.append(df)

#Renaming columns
btc_table.columns=['Index','Pool','Hashrate_Share','Blocks_Mined','Empty_Blocks_Count',
'Empty_Blocks_Perc','Ave_Block_Size','Ave_Tx_Fee_Per_Block','Tx_Fees_Perc_Block_Reward']

btc_table=btc_table[btc_table['Pool'].notna()]

print(btc_table)

parent=os.path.normpath(os.getcwd())
btc_table.to_csv(os.path.join(parent, os.path.join('Output','btc_pool_distribution.csv')),index=False)
