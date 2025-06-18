import pickle
import streamlit as st
import pandas as pd
from catboost import CatBoostRegressor
import plotly.express as px
model = CatBoostRegressor()
model.load_model('catboost_model.bin')



df = pd.read_csv("DatasetClean.csv")
# User input form
st.title("Dashboard Data Analytics")
st.header("Table query")
st.sidebar.header("please filter your column here :")
BRAND = st.sidebar.multiselect(
    "select the brand:",
    options=df["brand"].unique(),
    default=df["brand"].unique()
)

CATEGORY= st.sidebar.multiselect(
    "select the category:",
    options=df["category"].unique(),
    default=df["category"].unique()
)
SEASON = st.sidebar.multiselect(
    "select the season:",
    options=df["season"].unique(),
    default=df["season"].unique()
)
MATERIAL = st.sidebar.multiselect(
    "select the material:",
    options=df["material"].unique(),
    default=df["material"].unique()
)
STORE = st.sidebar.multiselect(
    "select the store type:",
    options=df["store_type"].unique(),
    default=df["store_type"].unique()
)
COLOR = st.sidebar.multiselect(
    "select the color type:",
    options=df["color"].unique(),
    default=df["color"].unique()
)
LOCATION = st.sidebar.multiselect(
    "select the location type:",
    options=df["location"].unique(),
    default=df["location"].unique()
)


df_selection = df.query(
    "brand == @BRAND & category == @CATEGORY & season == @SEASON & material == @MATERIAL & store_type == @STORE & color == @COLOR & location == @LOCATION   "
)

st.dataframe(df_selection)
col1, col2 = st.columns(2)

with col1:
    if not df_selection.empty:
        st.subheader("Bar Chart: Count per Category")
        bar_data = df_selection['category'].value_counts().reset_index()
        bar_data.columns = ['category', 'count']
        fig_bar = px.bar(bar_data, x='category', y='count', title='Items per Category')
        st.plotly_chart(fig_bar)
    else:
        st.warning("No data available for bar chart.")
with col2:
    st.subheader("Pie Chart : color distribution")
    if not df_selection.empty:
        pie_data = df_selection['color'].value_counts().reset_index()
        pie_data.columns = ['color', 'count']
        fig_pie = px.pie(pie_data, names='color', values='count', title='color Share')
        st.plotly_chart(fig_pie)
    else:
        st.warning("No data for pie chart.")

col3, col4 = st.columns(2)

with col3:
    if not df_selection.empty:
        st.subheader("Bar Chart: Count per brand")
        bar_data = df_selection['brand'].value_counts().reset_index()
        bar_data.columns = ['brand', 'count']
        fig_bar = px.bar(bar_data, x='brand', y='count', title='Items per brand')
        st.plotly_chart(fig_bar)
    else:
        st.warning("No data available for bar chart.")
with col4:
    st.subheader("Pie Chart : material distribution")
    if not df_selection.empty:
        pie_data = df_selection['material'].value_counts().reset_index()
        pie_data.columns = ['material', 'count']
        fig_pie = px.pie(pie_data, names='material', values='count', title='material Share')
        st.plotly_chart(fig_pie)
    else:
        st.warning("No data for pie chart.")
        
col5, col6 = st.columns(2)

with col5:
    if 'price' in df_selection.columns:
        st.subheader("Histogram: Price Distribution")
        fig_hist = px.histogram(df_selection, x='price', nbins=20, title='Price Histogram')
        st.plotly_chart(fig_hist)
    else:
        st.warning("No 'price' column found.")
with col6:
    if 'sales' in df_selection.columns:
        st.subheader("Histogram: sales Distribution")
        fig_hist = px.histogram(df_selection, x='sales', nbins=20, title='sales Histogram')
        st.plotly_chart(fig_hist)
    else:
        st.warning("No 'price' column found.")
col7, col8 = st.columns(2)
with col7:
    st.subheader("Pie Chart : location distribution")
    if not df_selection.empty:
        pie_data = df_selection['location'].value_counts().reset_index()
        pie_data.columns = ['location', 'count']
        fig_pie = px.pie(pie_data, names='location', values='count', title='location Share')
        st.plotly_chart(fig_pie)
    else:
        st.warning("No data for pie chart.")
with col8:
    st.subheader("Pie Chart : season distribution")
    if not df_selection.empty:
        pie_data = df_selection['season'].value_counts().reset_index()
        pie_data.columns = ['season', 'count']
        fig_pie = px.pie(pie_data, names='season', values='count', title='season Share')
        st.plotly_chart(fig_pie)
    else:
        st.warning("No data for pie chart.")
col9, col10 = st.columns(2)

with col9:
    if 'cost' in df_selection.columns:
        st.subheader("Histogram: cost Distribution")
        fig_hist = px.histogram(df_selection, x='cost', nbins=20, title='Cost Histogram')
        st.plotly_chart(fig_hist)
    else:
        st.warning("No 'price' column found.")
with col10:
    if 'revenue' in df_selection.columns:
        st.subheader("Histogram: revenue Distribution")
        fig_hist = px.histogram(df_selection, x='revenue', nbins=20, title='revenue Histogram')
        st.plotly_chart(fig_hist)
    else:
        st.warning("No 'price' column found.")

st.header("SALES Prediction")

st.subheader("this is a sales prediction webapp for our sales prediction model")

price = st.number_input("Price  ", value=477.0)
cost = st.number_input("Cost", value=385.03)
profit_margin = st.number_input("Profit Margin", value=19.41)
inventory = st.number_input("Inventory", value=192)
discount_percentage = st.number_input("Discount Percentage", value=26.94)
delivery_days = st.number_input("Delivery Days", value=6)
revenue = st.number_input("Revenue", value=-3521)

category = st.selectbox("Category", ['Chair', 'Table', 'Sofa','Bed','Desk'])  
material = st.selectbox("Material", ['Glass', 'Wood', 'Plastic','Metal','Fabric']) 
color = st.selectbox("Color", ['Blue', 'Red', 'White','Green','Black','Brown'])  
location = st.selectbox("Location", ['Rural', 'Urban','Suburban'])  
season = st.selectbox("Season", ['Summer', 'Winter', 'Spring', 'Fall'])  
store_type = st.selectbox("Store Type", ['Online', 'Retail']) 
brand = st.selectbox("Brand", ['BrandA', 'BrandB', 'BrandC', 'BrandD'])  

if st.button("Predict Revenue"):
    input_data = pd.DataFrame({
        'price': [price],
        'cost': [cost],
        'profit_margin': [profit_margin],
        'inventory': [inventory],
        'discount_percentage': [discount_percentage],
        'delivery_days': [delivery_days],
        'category': [category],
        'material': [material],
        'color': [color],
        'location': [location],
        'season': [season],
        'store_type': [store_type],
        'brand': [brand],
        'revenue' :[revenue],
    })
    
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted sales: {prediction:.2f}")
    
    