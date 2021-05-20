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



#To create year, month, day and hour columns
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
st.sidebar.title("Menu")
pressed= st.sidebar.radio("Navigate", ["Data Exploration", "Market Basket Analysis"])
st.sidebar.title("About")
st.sidebar.info("This Streamlit application allows users to explore a bakery's transactional data that was collected from October 2016 till April 2017.")
if "Market Basket Analysis" in pressed:
    
#---------------------------------------------------------------#
# SELECT Month AND SETUP DATA
#---------------------------------------------------------------#

 st.set_option('deprecation.showPyplotGlobalUse', False)
    


best_selling = Bakery_data.Item.unique()


number_items=len(Bakery_data["Item"].unique())
#To check the number of unique transactions:
unique_trans=len(Bakery_data["Transaction"].unique())

monthly_trans=month_year.groupby('Monthly')['Item'].count().sort_values()
timing_df= part_of_day['Daytime'].value_counts()[:1]




st.markdown('#') 

if "Data Exploration" in pressed:
    col1, col2 = st.beta_columns([0.5,0.5])
    

    with col1:
        st.markdown("<h1 style='text-align: left; color: #ef7c76;font-size:60'>Coffee</h1>", unsafe_allow_html=True)
        st.markdown("Most Selling Item")
        st.write(number_items)
        st.markdown("Different Products")
        st.write(unique_trans)
        st.markdown("Total Transactions")
        st.markdown("<h1 style='text-align: left; color: #ec514e;font-size:60'>12 pm - 5 pm</h1>", unsafe_allow_html=True)
        st.markdown("Peak Hours")
        st.markdown("<h1 style='text-align: left; color: #937346;font-size:60'>Coffee & Toast</h1>", unsafe_allow_html=True)
        st.markdown("Best Selling Combination")

    
        
    with col2:
        st.markdown("<h3 style='text-align:left'>Top Five Selling Items</h3>", unsafe_allow_html=True) 
        fig = px.bar(top_items,x= top_items.index.values.tolist(), y=['Item'],width=600, height=400,labels={ 
                "value":"Number of Items Sold","x":"Items"})
        fig.update_traces(marker_color='#cc4c02')
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
         })
        st.plotly_chart(fig)  

st.markdown('#')
#To create the sales transactions per month  
if "Data Exploration" in pressed:
    
    col3, col4 = st.beta_columns([0.5,0.5])   

    with col3:
        st.markdown("### **Sales Transactions Per Month:**")
        st.write("Which month would you like to view?")
        sorted_month = month_year['Monthly'].unique()
        select_option = []
        select_option.append(st.selectbox('', sorted_month))
        month_df=month_year[month_year['Monthly'].isin(select_option)]
        st.markdown(f"**Total Transactions:** {month_df.shape[0]}")

        
#To create the sales transactions per days
if "Data Exploration" in pressed:
    with col4:
        st.markdown("### **Sales Transactions Per Day:**")
        st.write('Which day would you like to view?')
        sorted_day = week_day['Weekday']
        select_options = []
        select_options.append(st.selectbox('', sorted_day))
        day_df=week_day[week_day['Weekday'].isin(select_options)]
        st.markdown(f"**Total Day Transactions:** {day_df.iloc[0]['Transaction']}")

    

#To create the peak hours per item   
if "Data Exploration" in pressed:
    st.markdown("### **Peak Hours Per Item:**")
    selected_status= st.selectbox('Which item would you like to view?', options=['Coffee', 'Bread','Cake', 'Tea'])
     
   
    if 'Tea' in selected_status:
        st.subheader('Tea Peak Hours')
        fig = px.bar(tea_hours,x= tea_hours['Daytime'], y=['Item'],
            labels={ 
                "value":"Number of Items Sold"})
        fig.update_traces(marker_color="#fe9929")
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
         })
        st.plotly_chart(fig)
        

    if 'Coffee' in selected_status:
        fig = px.bar(coffee_hours,x= coffee_hours['Daytime'], y=['Item'],labels={ 
                "value":"Number of Items Sold"})
        fig.update_traces(marker_color="#ef7c76")
        fig.update_layout({
       'plot_bgcolor': 'rgba(0, 0, 0, 0)',
       'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
        st.plotly_chart(fig)
 
    


    
    if 'Cake' in selected_status:
        fig = px.bar(cake_hours,x= cake_hours['Daytime'], y=cake_hours['Item'],labels={ 
                "value":"Number of Items Sold"})
        fig.update_traces(marker_color="#cc4c02")
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
         })
        st.plotly_chart(fig)
  
    

    if "Bread" in selected_status:
        fig = px.bar(bread_hours,x= bread_hours['Daytime'], y=bread_hours['Item'],labels={"value":"Number of Items Sold"})
        fig.update_traces(marker_color="#937346")
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
          })
        st.plotly_chart(fig)
   
        


        
#To write the fun facts about the customers' behaviors
if "Market Basket Analysis" in pressed:
    st.markdown("### **Association Rules:**")
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

#To include the up-sell and cross-sell strategies
if "Market Basket Analysis" in pressed:    
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

#To include a disclaimer expander at the bottom
expander = st.beta_expander("Disclaimer:")
expander.markdown("This project is for Data Driven Digital Marketing Course at OSB-AUB")






