import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

st.title("Property sales in Melbourne City")

DATA_URL = ("https://csvdata12.s3.ap-south-1.amazonaws.com/Property+Sales+of+Melbourne+City.csv")
DATE_COLUMN="Date"

@st.cache_data
def load_data(n_rows):
    data = pd.read_csv(DATA_URL, nrows=n_rows)
    return data


data = load_data(10000)

# Handling null values

null = pd.DataFrame({'Null Values': data.isnull().sum(), 'Percentage null values': data.isnull().sum() * 100 / len(data)})
null = null.sort_values('Percentage null values', ascending=False)
# st.write(null)

data['BuildingArea'] = data['BuildingArea'].fillna(data['BuildingArea'].median())
data['YearBuilt'] = data['YearBuilt'].fillna(data["YearBuilt"].median())
data['CouncilArea'] = data['CouncilArea'].fillna(data['CouncilArea'].mode()[0])
data['Landsize'] = data['Landsize'].fillna(data['Landsize'].median())
data.dropna(inplace=True)


#Feature Engineering
data.drop("Unnamed: 0", axis=1, inplace=True)
data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format="%d/%m/%Y")
data["Year"] = data[DATE_COLUMN].dt.year
data["Month"]  =  data[DATE_COLUMN].dt.month
data['TotalRooms'] = data['Rooms'] + data['Bathroom'] + data['Bedroom2']
data['Type'] = data['Type'].map({'h':'house','t':'townhouse','u':'apartment'})
data['Method'] = data['Method'].map({'S':'property sold','SP':'property sold prior','PI':'property passed in',
                                 'VB':'vendor bid','SA':'sold after auction'})
data.drop(['Address','Date','Postcode','YearBuilt'],axis=1,inplace=True)


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

    st.subheader('Data info')
    st.write(data.describe())

st.subheader("Top 10 Property Suburbs which has the highest average sales price yearly")

year_to_filter = st.selectbox("Select Year", [2016, 2017])

filtered_data = data[data["Year"] == year_to_filter]

suburb_prices = filtered_data.groupby('Suburb')['Price'].mean().reset_index()

# Sort the data by the average price in descending order
suburb_prices = suburb_prices.sort_values(by='Price', ascending=False)

top_10 = suburb_prices.head(10)
# Display the bar chart using streamlit
st.bar_chart(top_10, x="Suburb", y="Price")


st.subheader("Top 10 Property Suburbs which has the highest most property count")

suburb_property_count = filtered_data.groupby('Suburb')['Propertycount'].mean().reset_index().sort_values(by="Propertycount", ascending=False).head(10)

st.bar_chart(suburb_property_count, x="Suburb", y="Propertycount")


st.subheader("Highest Property in a Region")

reg_prop = round(data.groupby('Regionname')['Propertycount'].mean(),2)
reg_prop = reg_prop.reset_index().sort_values('Propertycount',ascending=False).reset_index(drop=True)

st.bar_chart(reg_prop, x="Regionname", y="Propertycount")

st.subheader("Highest Price in a Region")

region_high_price = data.groupby("Regionname")["Price"].sum().reset_index().sort_values("Price", ascending=False).reset_index(drop=True).head(10)

st.bar_chart(region_high_price, x="Regionname", y="Price")

st.subheader("Most Sold Type Of Property")
property_type_counts = data["Type"].value_counts().reset_index().rename(columns={'index':'Type','Type':'count'})
# st.write(property_type_counts)
st.bar_chart(property_type_counts, x="Type", y="count")

st.subheader("Most used method for Sales")

most_used_method = data['Method'].value_counts().reset_index().rename(columns={'index': "Method", "Method": "Properties Sold"})
st.bar_chart(most_used_method, x="Method", y="Properties Sold")

st.subheader("Type which has the highest sell price")

type_high_price = data.groupby("Type")["Price"].sum().reset_index().sort_values(by="Price", ascending=False).reset_index(drop=True)

# st.write(type_high_price)
st.bar_chart(type_high_price, x="Type", y="Price")

st.subheader("Top 10 Agency which sold the most property")
agency_most_property_sold = data["SellerG"].value_counts().reset_index().rename(columns={'index': "Agency", "SellerG": "Count"}).head(10)

# st.write(agency_most_property_sold)
st.bar_chart(agency_most_property_sold, x="Agency", y="Count")