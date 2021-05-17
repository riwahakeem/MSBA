import numpy as np
from PIL import Image
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import requests
from io import StringIO
import plotly.graph_objs as go
import chart_studio.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
plotly.offline.init_notebook_mode(connected=True)
from PIL import Image
from typing import List, Optional
import markdown

orig_url='https://drive.google.com/file/d/168P5Pt62UwwIKktFmFHTyR1_Kt2TLGqY/view?usp=sharing'

file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
url = requests.get(dwn_url).text
csv_raw = StringIO(url)
Bakery_data = pd.read_csv(csv_raw)



st.set_page_config(page_title="Bakery Market Basket Analysis", 
                   page_icon=":bread:")


month_year=Bakery_data.copy()
month_year['Year'] = month_year.Date.apply(lambda x:x.split('/')[2])
month_year['Month'] = month_year.Date.apply(lambda x:x.split('/')[0])
month_year['Day'] = month_year.Date.apply(lambda x:x.split('/')[1])
month_year['Hour'] =month_year.Time.apply(lambda x:int(x.split(':')[0]))


#To change the month numbers into words and creating a new column named Monthly
month_year.loc[month_year.Month == '10', 'Monthly'] = 'October'  
month_year.loc[month_year.Month == '11', 'Monthly'] = 'November' 
month_year.loc[month_year.Month == '12', 'Monthly'] = 'December' 
month_year.loc[month_year.Month == '1', 'Monthly'] = 'January' 
month_year.loc[month_year.Month == '2', 'Monthly'] = 'Febraury' 
month_year.loc[month_year.Month == '3', 'Monthly'] = 'March' 
month_year.loc[month_year.Month == '4', 'Monthly'] = 'April'  

# To get the top 5 bought items:
top_items = Bakery_data.Item.value_counts()[:5]

values = top_items.tolist()
#Labels include top five items name.
labels = top_items.index.values.tolist()

#To divide the time into morning, afternoon, evening and night
part_of_day=Bakery_data.copy()
part_of_day.loc[part_of_day['Time']<'12:00:00','Daytime']='Morning'
part_of_day.loc[(part_of_day['Time']>='12:00:00')&(part_of_day['Time']<'17:00:00'),'Daytime']='Afternoon'
part_of_day.loc[(part_of_day['Time']>='17:00:00')&(part_of_day['Time']<'20:00:00'),'Daytime']='Evening'
part_of_day.loc[(part_of_day['Time']>='20:00:00')&(part_of_day['Time']<'23:50:00'),'Daytime']='Night'


#To group the transactions per each day
week_day=Bakery_data.copy()
week_day=week_day.groupby('Weekday')['Transaction'].count()
week_day=week_day.reset_index()

#To group the transactions that contain Coffee only
coffee_hours=part_of_day[part_of_day['Item']=='Coffee']
coffee_hours=coffee_hours.groupby('Daytime')['Item'].count()
coffee_hours=coffee_hours.reset_index()


#Question 7:
#peak Bread hours
#To group the transactions that contain Bread
bread_hours=part_of_day[part_of_day['Item']=='Bread']
bread_hours=bread_hours.groupby('Daytime')['Item'].count()
bread_hours=bread_hours.reset_index() 

#To group the transactions that contain Cake
cake_hours=part_of_day.loc[(part_of_day['Item']=='Cake') | (part_of_day['Item']=='Pastry')]
cake_hours=cake_hours.groupby('Daytime')['Item'].count()
cake_hours=cake_hours.reset_index()

#Question 9:
#peak tea hours
#To group the transactions that contain tea
tea_hours=part_of_day.loc[(part_of_day['Item']=='Tea')]
tea_hours=tea_hours.groupby('Daytime')['Item'].count()
tea_hours=tea_hours.reset_index()

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------
st.title('Bakery Market Basket Analysis')
st.markdown("by Riwa Al Hakeem | May 2021")

#---------------------------------------------------------------#
# SELECT Month AND SETUP DATA
#---------------------------------------------------------------#

st.set_option('deprecation.showPyplotGlobalUse', False)
      
"""
This Streamlit application allows users to explore a bakery's transactional data that was collected from October 2016 till April 2017.

"""
st.markdown('#') 
col1, col2 = st.beta_columns([0.5,0.5])
    

with col1:
    """ 
    
    """
    st.markdown("<h1 style='text-align: left; color: #ef7c76;font-size:60'>Coffee</h1>", unsafe_allow_html=True)
    st.markdown("Most Selling Item")
    st.markdown("<h1 style='text-align: left; color: #783500;font-size:60'>94</h1>", unsafe_allow_html=True)
    st.markdown("Different Products")
    st.markdown("<h1 style='text-align: left; color: #fe9929 ;font-size:60'>9684 </h1>", unsafe_allow_html=True)
    st.markdown("Total Transactions")
    st.markdown("<h1 style='text-align: left; color: #ec514e;font-size:60'>12 pm - 5 pm</h1>", unsafe_allow_html=True)
    st.markdown("Peak Hours")
        
with col2:
    st.markdown("<h3 style='text-align:left'>Top Five Selling Items</h3>", unsafe_allow_html=True) 
    Top_5= top_items
    y_axis = labels
    x_axis = values
    plt.bar(y_axis,x_axis,color='#cc4c02')
    plt.ylabel('Item')
    plt.xlabel('Total Items Sold')
    st.pyplot() 
    """
    
    """
    st.markdown("<h1 style='text-align: left; color: #937346;font-size:60'>Coffee & Toast</h1>", unsafe_allow_html=True)
    st.markdown("Best Selling Combination")
        
st.markdown('#')
    
col3, col4 = st.beta_columns([0.5,0.5])   
with col3:
    st.markdown("### **Sales Transactions Per Month:**")
    option = st.selectbox('Which month would you like to view?', month_year['Monthly'].unique())

    if 'October' in option:
        st.write("The total number of transactions in **_October_** was **_369_**.")
    if 'November' in option:
        st.write("The total number of transactions in **_November_** was **_4436_**.")
    if 'March' in option:
        st.write("The total number of transactions in **_March_** was **_3944_**.")
    if 'January' in option:
        st.write("The total number of transactions in **_January_** was **_3356_**.")
    if 'Febraury' in option:
        st.write("The total number of transactions in **_Febraury_** was **_3906_**.")
    if 'December' in option:
        st.write("The total number of transactions in **_December_** was **_3339_**.")
    if 'April' in option:
        st.write("The total number of transactions in **_April_** was **_1157_**.")
        
with col4:        
    st.markdown("### **Sales Transactions Per Day:**")
    option_day = st.selectbox('Which option would you like to view?', options=['Busiest Day', 'Least Busy Day'])
    if "Busiest Day" in option_day:
        st.write("**_Saturday_** is the busiest day at the Bakery!")
    if "Least Busy Day" in option_day:
        st.write("**_Wednesday_** is the least busy day at the Bakery!")

st.markdown("### **Peak Hours Per Item:**")
selected_status= st.selectbox('Which item would you like to view?', options=['Coffee', 'Bread','Cake', 'Tea'])
if 'Tea' in selected_status:
        st.subheader('Tea Peak Hours')
        fig,ax=plt.subplots(figsize=(6,4))
        ax=sns.barplot(data=tea_hours,x='Daytime',y='Item', color="#fe9929")
        ax.set_xlabel('Hours Of The Day',fontsize=12,color='#262730')
        ax.set_ylabel('Number of Times Tea is Sold',fontsize=12,color='#262730')
        ax.set_title('Tea Peak Hours')
        st.pyplot()
        
if 'Coffee' in selected_status:
    fig,ax=plt.subplots(figsize=(6,4))
    ax=sns.barplot(data=coffee_hours,x='Daytime',y='Item',color="#ef7c76")
    ax.set_xlabel('Hours Of The Day',fontsize=12,color='#262730')
    ax.set_ylabel('Number of Times Coffee is Sold',fontsize=12,color='#262730')
    ax.set_title('Coffee Peak Hours')
    st.pyplot()
    
if 'Cake' in selected_status:
    fig,ax=plt.subplots(figsize=(6,4))
    ax=sns.barplot(data=cake_hours,x='Daytime',y='Item', color="#cc4c02")
    ax.set_xlabel('Hours Of The Day',fontsize=12,color='#262730')
    ax.set_ylabel('Number of Times Cake is Sold',fontsize=12,color='#262730')
    ax.set_title("Cake Peak Hours")
    st.pyplot()
    
if "Bread" in selected_status:
    fig,ax=plt.subplots(figsize=(6,4))
    ax=sns.barplot(data=bread_hours,x='Daytime',y='Item',color="#937346")
    ax.set_xlabel('Hours Of The Day',fontsize=12,color='#262730')
    ax.set_ylabel('Number of Times Bread is Sold',fontsize=12,color='#262730')
    ax.set_title('Bread Peak Hours')
    st.pyplot()
        

st.markdown("### **Fun Facts:**")
selected_status = st.selectbox('Which item would you like to view?',
                                       options = ['Toast', "Cake",'Spanish Brunch',
                                                   'Medialuna'])
if selected_status == 'Toast':
    st.write("**_70%_** of customers who bought **_Toast_** also bought **_Coffee_**.")
                                                
if selected_status == 'Spanish Brunch':
    st.write("**_60%_** of customers who bought **_Spanish_** **_Brunch_** also bought **_Coffee_**.")  

if selected_status == 'Cake':
    st.write("**_53%_** of customers who bought **_Cake_** also bought **_Coffee_**.")  

if selected_status == 'Medialuna':
    st.write("**_57%_** of customers who bought **_Medialuna_** also bought **_Coffee_**.")  


st.markdown('### **Upsell and Cross-sell Strategies:**')
selected_status_1 = st.selectbox('Which item would you like to upsell/cross-sell?',
                                       options = ['Pastry', 'Spanish Brunch',
                                                   'Sandwich'])
if selected_status_1 == 'Pastry':
    st.write("The combination of **_Coffee_** and **_Pastry_** has a lift of **_1.15_**. This means that Pastry is 1.15 times more likely to be purchased when coffee is bought. Moreover, the combination of **_Bread_**, **_Coffee_** and **_Pastry_** has a lift of **_1.45_**. This means that pastry is 1.45 times more likely to be purchased when bread and coffee are bought.")
    st.markdown("** Potential Strategy:**")
    st.markdown("A promising strategy would be coffee promotions to encourage people to buy pastry. Also, the bakery could make a promotional bundles of bread and coffee to further encourage people to buy pastry.")
    
    
if selected_status_1 == 'Spanish Brunch':
    st.write("The combination of **_Coffee_** and **_Spanish_** **_brunch_** has a lift of **_1.25_**. This means that Spanish Brunch is 1.25 times more likely to be purchased when coffee is bought.")
    st.markdown("** Potential Strategy:**")
    st.markdown("A promising strategy would be to run coffee promotion or a combo meal that includes coffee and Spanish brunch to upsell their Spanish brunch.")
    
    
if selected_status_1 == 'Sandwich':
    st.write("The combination of **_Sandwich_** and **_Tea_**  has a lift of **_1.4_**. This means that Sandwich is 1.4 times more likely to be purchased when tea is bought. Moreover, the combination of **_Coffee_** and **_Sandwich_** has a lift of **_1.13_**. This means that sandwich is 1.13 times more likely to be purchased when coffee is bought.")
    st.markdown("** Potential Strategy:**")
    st.markdown("A promising strategy would be to run tea and coffee promotions to encourage people to buy sandwiches.")  

st.markdown('#')
st.markdown('#')

expander = st.beta_expander("Disclaimer:")
expander.markdown("This project is for Data Driven Digital Marketing Course at OSB-AUB")