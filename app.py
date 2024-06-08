import streamlit as st
import pandas as pd
import plotly.express as px

vehicles_df = pd.read_csv("vehicles_us.csv")

#Replace missing values 

#with mode for 'is_4wd'
vehicles_df['is_4wd'].fillna(vehicles_df['is_4wd'].mode()[0], inplace=True)

#with mode for 'cylinders'
vehicles_df['cylinders'].fillna(vehicles_df['cylinders'].mode()[0], inplace=True)

#with median for 'model_year'
vehicles_df['model_year'] = vehicles_df['model_year'].fillna(2011)

#with median for 'odometer'
vehicles_df['odometer'] = vehicles_df['odometer'].fillna(113000)


#Histogram of prices

price_histo = px.histogram(vehicles_df, x='price',  
                           labels={'x':'Price'}, 
                           nbins = 150, 
                           range_x = [0, 95000],
                          )

#Scatterplot of prices vs days listed

price_dayslisted_scatter = px.scatter(vehicles_df, 
                                      x='days_listed', 
                                      labels={'x':'days listed'}, 
                                      y='price', 
                                      )


#Box plot of condition vs price

condition_price_box = px.box(vehicles_df, 
                             x='condition', 
                             y='price', 
                             )

#Scatterplot of price vs mileage

price_miles_scatter = px.scatter(vehicles_df, 
                                 x='odometer', 
                                 y='price', 
                                 range_x = [0, 500000]
                                 )




#Streamlit code

st.header('Used Vehicles Dataset', anchor=False, divider='rainbow')
st.header('Comprehensive Vehicle Pricing Information', anchor=False, divider=False)

st.write('Prices')
st.plotly_chart(price_histo, theme = 'streamlit')

st.write('Prices vs Condition')
st.plotly_chart(condition_price_box, theme = 'streamlit')

st.write('Prices vs Mileage')
st.plotly_chart(price_miles_scatter, theme = 'streamlit')

st.write('Prices vs Days Listed')
st.plotly_chart(price_dayslisted_scatter, theme = 'streamlit')

sample = st.checkbox("View sample dataset")

if sample:
    st.write(vehicles_df.sample(20))


