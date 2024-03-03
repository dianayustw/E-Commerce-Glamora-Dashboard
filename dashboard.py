# ==========================================[ Import Library ]================================================== 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from babel.numbers import format_currency
import warnings
warnings.filterwarnings('ignore')
sns.set(style='dark')

# ============================================[ Page Setup ]=====================================================
st.set_page_config(page_title="Glamora", page_icon=":shopping_bags:", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ==========================================[ Helper function ]================================================== 
# Monthly Orders 2016 Function __________________________________________________________________________________
def create_monthly_orders_16_df(df):
    monthly_orders_16_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()

    monthly_orders_16_df = monthly_orders_16_df[monthly_orders_16_df['order_purchase_timestamp'].apply(lambda x: str(x.year).startswith('2016'))]
    monthly_orders_16_df['order_purchase_timestamp'] = pd.to_datetime(monthly_orders_16_df['order_purchase_timestamp']).dt.strftime('%B')

    monthly_orders_16_df.rename(columns={
        "order_purchase_timestamp": "order_date",
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return monthly_orders_16_df

# Monthly Orders 2017 Function __________________________________________________________________________________
def create_monthly_orders_17_df(df):
    monthly_orders_17_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()

    monthly_orders_17_df = monthly_orders_17_df[monthly_orders_17_df['order_purchase_timestamp'].apply(lambda x: str(x.year).startswith('2017'))]
    monthly_orders_17_df['order_purchase_timestamp'] = pd.to_datetime(monthly_orders_17_df['order_purchase_timestamp']).dt.strftime('%B')

    monthly_orders_17_df.rename(columns={
        "order_purchase_timestamp": "order_date",
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return monthly_orders_17_df

# Monthly Orders 2018 Function __________________________________________________________________________________
def create_monthly_orders_18_df(df):
    monthly_orders_18_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()

    monthly_orders_18_df = monthly_orders_18_df[monthly_orders_18_df['order_purchase_timestamp'].apply(lambda x: str(x.year).startswith('2018'))]
    monthly_orders_18_df['order_purchase_timestamp'] = pd.to_datetime(monthly_orders_18_df['order_purchase_timestamp']).dt.strftime('%B')

    monthly_orders_18_df.rename(columns={
        "order_purchase_timestamp": "order_date",
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return monthly_orders_18_df

# Payment Type Function _________________________________________________________________________________________
def create_payment_type_df(df):
    payment_type_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    payment_type_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return payment_type_df

# Delivery Status Function ______________________________________________________________________________________
def create_delivery_status_df(df):
    delivery_status_df = df.groupby(by="delivery_status").order_id.nunique().reset_index()
    delivery_status_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    delivery_status_df['delivery_status'] = pd.Categorical(delivery_status_df['delivery_status'], ["On Time", "Delayed"])

    return delivery_status_df

def create_delivery_time_status_df(df):
    on_time_df = df.loc[df['delivery_status'] == 'On Time']
    delayed_df = df.loc[df['delivery_status'] == 'Delayed']

    return on_time_df, delayed_df


# ==========================================[ Load Cleaned Data ]================================================ 
all_df = pd.read_csv("https://raw.githubusercontent.com/dianayustw/E-Commerce-All-Orders/master/all_orders.csv")

# ============================================[ Datetime Data ]==================================================
datetime_columns = ["shipping_limit_date", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# ==============================================[ Side Bar ]=====================================================
with st.sidebar:
    # Logo
    st.image("https://raw.githubusercontent.com/dianayustw/E-Commerce-Public-Dataset/master/glamora-logo.png")
    
    # start_date & end_date
    st.subheader('Time Range')
    start_date = st.date_input(label='Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input(label='End Date', min_value=min_date, max_value=max_date, value=max_date)

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# =============================================[ DataFrames ]====================================================
monthly_orders_16_df = create_monthly_orders_16_df(main_df)
monthly_orders_17_df = create_monthly_orders_17_df(main_df)
monthly_orders_18_df = create_monthly_orders_18_df(main_df)
payment_type_df = create_payment_type_df(main_df)
delivery_status_df = create_delivery_status_df(main_df)
delivery_time_status_df = create_delivery_time_status_df(main_df)

# ============================================[ Visualization ]==================================================
# Header ________________________________________________________________________________________________________
st.header('Glamora E-Commerce Dashboard :shopping_bags:')

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        total_orders = main_df.order_id.count()
        st.metric("Total Orders", value=total_orders)

with col2:
    with st.container(border=True):
        total_transactions = format_currency(main_df.payment_value.sum(), "US $", locale='es_US') 
        st.metric("Total Sales", value=total_transactions)

with col3:
    with st.container(border=True):
        average_transactions = format_currency(main_df.payment_value.mean(), 'US $', locale='en_US')
        st.metric("Average Sales", value=average_transactions)

# Number of Orders and Total Revenue per Month __________________________________________________________________
dataframes = [monthly_orders_16_df, monthly_orders_17_df, monthly_orders_18_df]

def create_line_plot(df, year):
    if df is not None and year is not None:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Number of Orders", "Total Revenue"))
        
        fig.add_trace(
            go.Scatter(x=df['order_date'], y=df['order_count'], mode='lines', name='Order Count'),
            row=1, col=1
        )
        fig.update_xaxes(title_text="Order Date", row=1, col=1)
        fig.update_yaxes(title_text="Order Count", row=1, col=1)

        fig.add_trace(
            go.Scatter(x=df['order_date'], y=df['revenue'], mode='lines', name='Revenue', line=dict(color='#E61580')),
            row=1, col=2
        )
        fig.update_xaxes(title_text="Order Date", row=1, col=2)
        fig.update_yaxes(title_text="Revenue", row=1, col=2)

        fig.update_layout(width=900, showlegend=False, title=f' Number of Orders and Total Revenue per Month ({year})')
        return fig
    
years_available = []

if str(start_date).startswith('2016') and str(end_date).startswith('2016'):
    years_available.extend(['2016'])
if str(start_date).startswith('2017') and str(end_date).startswith('2017'):
    years_available.extend(['2017'])
if str(start_date).startswith('2018') and str(end_date).startswith('2018'):
    years_available.extend(['2018'])
if str(start_date).startswith('2016') and str(end_date).startswith('2017'):
    years_available.extend(['2016', '2017'])
if str(start_date).startswith('2016') and str(end_date).startswith('2018'):
    years_available.extend(['2016', '2017', '2018'])
if str(start_date).startswith('2017') and str(end_date).startswith('2018'):
    years_available.extend(['2017', '2018'])

selected_year = st.selectbox('Select Year', years_available)
selected_df = dataframes[int(selected_year) - 2016]
fig = create_line_plot(selected_df, selected_year)
st.plotly_chart(fig, use_container_width=True, width=800, height=600)

# Ratio of Payment Types _________________________________________________________________________________________
fig = px.pie(
    payment_type_df,
    values='order_count',
    names='payment_type',
    title='Ratio of Payment Types Based on Order Count',
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True, width=800, height=600)

# Delivery Status Comparison ______________________________________________________________________________________
with st.container():
    fig = px.bar(
        delivery_status_df.sort_values(by="delivery_status", ascending=False),
        y="order_count",
        x="delivery_status",
        title="Delivery Status Comparison",
        color_discrete_sequence=["#E61580"],
        labels={"order_count": "Number of Orders", "delivery_status": "Delivery Status"}
    )
    st.plotly_chart(fig, use_container_width=True, width=800, height=600)


genre = st.radio(
    "Delivery Time Status",
    ["On Time", "Delayed"]
)

on_time_df, delayed_df = create_delivery_time_status_df(main_df)

if genre == 'On Time':
    delivery_time_status = on_time_df
else:
    delivery_time_status = delayed_df

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        max_on_time = delivery_time_status.delivery_time.max()
        if pd.notnull(max_on_time):
            st.metric("Max Delivery Time", value=f"{int(max_on_time)} days")
        else:
            st.metric("Max Delivery Time", value="No data available")
with col2:
    with st.container(border=True):
        min_on_time = delivery_time_status.delivery_time.min()
        if pd.notnull(min_on_time):
            st.metric("Min Delivery Time", value=f"{int(min_on_time)} days")
        else:
            st.metric("Min Delivery Time", value="No data available")

with col3:
    with st.container(border=True):
        average_on_time = delivery_time_status.delivery_time.mean()
        if pd.notnull(average_on_time):
            st.metric("Average Delivery Time", value=f"{int(average_on_time)} days")
        else:
            st.metric("Average Delivery Time", value="No data available")

st.caption('Copyright © 2024 Glamora. All rights reserved.')
