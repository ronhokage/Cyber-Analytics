# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:25:17 2021

@author: Rohan Jacob
"""

# #!pip install pywebio
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *

import pickle
import numpy as np
import pandas as pd
model = pickle.load(open('file_cyb.pkl', 'rb'))
data=pd.read_csv('D:\\601_prj.csv')
dp=pd.DataFrame(data=data,columns=["S_IP",'Source IP','Attack category','Attack_category','Service_1','Service'])
df_2 = dp.drop_duplicates(subset=["S_IP",'Source IP'])
df_3=  dp.drop_duplicates(subset=['Attack category','Attack_category'])
df_4=  dp.drop_duplicates(subset=['Service_1','Service'])
df1=df_2.sort_values(by='Source IP', ascending=True)
df2=df_3.sort_values(by='Attack category', ascending=True)
df3=df_4.sort_values(by='Service',ascending=True)
#pd.set_option("display.max_rows", None, "display.max_columns", None)
app = Flask(__name__)


def predict():
    k=select("Select Source Ip", df1['Source IP'])
    c=df1['S_IP'][df1['Source IP']==k].values[0]
    l=select("Select Attack category", df2['Attack category'])
    d=df2['Attack_category'][df2['Attack category']==l].values[0]
    m=select("Select Service",df3['Service'])
    n=df3['Service_1'][df3['Service']==m].values[0]
    prediction = model.predict([[c,d,n]])
    output = round(prediction[0],0)
    print(prediction)
  
    put_text('Predicted Label:',output)
    
    if output==0:
        put_text('Predicted severity is Low')
    else:
        put_text('Predicted severity is High')
app.add_url_rule('/tool', 'webio_view', webio_view(predict),
                     methods=['GET', 'POST', 'OPTIONS'])
app.run(host='localhost', port=80)

#visit http://localhost/tool