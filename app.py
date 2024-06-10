#Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#Import dataset
vehicles_df = pd.read_csv("vehicles_us.csv")

#Cleanse dataset

#Replace missing values 
#0 for 'is_4wd' because this is a boolean and currently all values are 1 or NaN so can presume the NaNs should be 0
vehicles_df['is_4wd'].fillna(0, inplace=True)

#with median for 'odometer'
vehicles_df['odometer'] = vehicles_df['odometer'].fillna(113000)

#median per 'cyclinder' and use to fill NaN
vehicles_df['cylinders'] = vehicles_df.groupby('type')['cylinders'].transform(lambda x: x.fillna(x.median()))

#median per 'model_year' and use to fill NaN
vehicles_df['model_year'] = vehicles_df.groupby('odometer')['model_year'].transform(lambda x: x.fillna(x.median()))

#There were still 876 missing values for 'model_year' after running above code; replacing remaining NaN with overall median
median_model_year = vehicles_df['model_year'].median()
vehicles_df['model_year'] = vehicles_df['model_year'].fillna(median_model_year)

#Remove outliers
#Create IQR variables for 'price', 'odometer', 'days_listed'
Q1_price = vehicles_df['price'].quantile(0.25)
Q3_price = vehicles_df['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price

Q1_odometer = vehicles_df['odometer'].quantile(0.25)
Q3_odometer = vehicles_df['odometer'].quantile(0.75)
IQR_odometer = Q3_odometer - Q1_odometer

Q1_days_listed = vehicles_df['days_listed'].quantile(0.25)
Q3_days_listed = vehicles_df['days_listed'].quantile(0.75)
IQR_days_listed = Q3_days_listed - Q1_days_listed

#Define outlier bounds
price_lower_bound = Q1_price - 1.5 * IQR_price
price_upper_bound = Q3_price + 1.5 * IQR_price

odometer_lower_bound = Q1_odometer - 1.5 * IQR_odometer
odometer_upper_bound = Q3_odometer + 1.5 * IQR_odometer

days_listed_lower_bound = Q1_days_listed - 1.5 * IQR_days_listed
days_listed_upper_bound = Q3_days_listed + 1.5 * IQR_days_listed

#Filter out outliers
filtered_outliers_df = vehicles_df[
    (vehicles_df['price'] >= price_lower_bound) & 
    (vehicles_df['price'] <= price_upper_bound) &
    (vehicles_df['odometer'] >= odometer_lower_bound) & 
    (vehicles_df['odometer'] <= odometer_upper_bound) &
    (vehicles_df['days_listed'] >= days_listed_lower_bound) & 
    (vehicles_df['days_listed'] <= days_listed_upper_bound)
]



#Streamlit web app code
#Header

st.header('Used Vehicles Dataset')
st.header('Comprehensive Vehicle Pricing Information')


#First visualization (Price Histogram) for web app
#Histogram w/ title and axes labels

price_histo = px.histogram(vehicles_df, x='price', 
                           title='Used Vehicle Price Range Counts', 
                           labels={'price':'Prices',
                                  'count': 'Volume'}, 
                           nbins = 150, 
                           range_x = [0, 95000],
                          )
#Streamlit code to display this first chart
st.write('Prices')
st.plotly_chart(price_histo, theme = 'streamlit')



#Second visualization (Proces vs Mileage) for web app
#Scatterplot w/ title and axes labels

price_miles_scatter = px.scatter(vehicles_df, 
                                 x='odometer', 
                                 y='price', 
                                 title='Price vs Mileage', 
                                 range_x = [0, 500000],
                                 labels = {'price': 'Prices',
                                           'odometer': 'Mileage'
                                 }
                                )

#Streamlit code to display this second chart
st.write('Prices vs Mileage')
st.plotly_chart(price_miles_scatter, theme = 'streamlit')


#Second visualization w/ outliers removed
price_miles_outliers = px.scatter(filtered_outliers_df, 
                                 x='odometer', 
                                 y='price', 
                                 title='Price vs Mileage (Outliers Removed)', 
                                 range_x = [0, 250000],
                                 labels = {'price': 'Prices',
                                           'odometer': 'Mileage'
                                 }
                                )

#Checkbok option to view second visualization with outliers removed
outliers_1 = st.checkbox("View this chart with outliers removed")
if outliers_1:
    st.plotly_chart(price_miles_outliers)


#Third visualization (Prices vs Days Listed) for web app
#Scatterplot of prices vs days listed w/ title and axes labels

price_dayslisted_scatter = px.scatter(vehicles_df, 
                                      x='days_listed', 
                                      y='price', 
                                      title='Price vs Days Listed',
                                      labels = {
                                          'days_listed': 'Days Listed',
                                          'price': 'Prices'
                                      }
                                     )
#Streamlit code to display this third chart
st.write('Prices vs Days Listed')
st.plotly_chart(price_dayslisted_scatter, theme = 'streamlit')

#Third visualization w/ outliers removed
price_dayslisted_outliers = px.scatter(filtered_outliers_df, 
                                      x='days_listed', 
                                      y='price', 
                                      title='Price vs Days Listed (Outliers Removed)',
                                      labels = {
                                          'days_listed': 'Days Listed',
                                          'price': 'Prices'
                                      }
                                     )

#Checkbok option to view thirs visualization with outliers removed
outliers_2 = st.checkbox("View this chart with outliers removed", key='checkbox_2')
if outliers_2:
    st.plotly_chart(price_dayslisted_outliers)


#Fourth visualization (Prices vs Condition) for web app
#Box plot w/ title and axes labels

condition_price_box = px.box(vehicles_df, 
                             x='condition', 
                             y='price', 
                             title='Condition vs Price',
                             labels = {
                                 'condition': 'Condition Categories',
                                 'price': 'Prices'
                             }
                            )


#Streamlit code to display this fourth chart
st.write('Prices vs Condition')
st.plotly_chart(condition_price_box, theme = 'streamlit')






