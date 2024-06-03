from pathlib import Path

import pandas as pd
import pandas_ta as ta
import streamlit as st
from lightweight_charts import Chart
from lightweight_charts.widgets import StreamlitChart

# Load the data
data_path = Path.cwd() / 'data/btcusdt_h1.parquet'
df = pd.read_parquet(data_path)

# Reset index and capitalize column names, keep the index columns as 'time'
df.reset_index(inplace=True, names=['time'])
df.columns = df.columns.str.lower()

# Ensure the 'time' column is in datetime format
df['time'] = pd.to_datetime(df['time'])

features = pd.DataFrame({
    'time': df['time'],
    'EMA_50': ta.ema(df['close'], 50),
    'EMA_100': ta.ema(df['close'], 100)
}).dropna()

def plot_chart(df, features):
    chart = Chart()
    chart = StreamlitChart(width=1200, height=800)  # Fixed size as fallback
    chart.legend(visible=True)
    chart.set(df)

    # Create line plots for selected features
    for feature in features.columns:
        if feature != 'time':
            line = chart.create_line(feature)  # Label must match the column of the values
            line.set(features[['time', feature]])

    chart.load()

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')  # Set layout to wide mode

# Sidebar inputs
with st.sidebar:
    st.header("Chart Configuration")
    
    # Streamlit inputs for date selection
    start_date = st.date_input("Start Date", value=df['time'].min().date())
    end_date = st.date_input("End Date", value=df['time'].max().date())

    # Streamlit checkboxes for additional features
    st.subheader("Select Features to Display")
    feature_checkboxes = {
        feature: st.checkbox(feature, value=True)
        for feature in features.columns if feature != 'time'
    }

# Ensure start date is not after end date
if start_date > end_date:
    st.error("Start date must not be after end date")
else:
    # Filter the dataframe based on the selected dates
    filtered_df = df[(df['time'] >= pd.Timestamp(start_date)) & (df['time'] <= pd.Timestamp(end_date))]
    filtered_features = features[(features['time'] >= pd.Timestamp(start_date)) & (features['time'] <= pd.Timestamp(end_date))]

    # Filter the features to display based on checkboxes
    selected_features = {feature: data for feature, data in feature_checkboxes.items() if data}
    selected_features_df = filtered_features[['time', *list(selected_features.keys())]]

    # Use Streamlit container to adjust chart to screen size
    with st.container():
        plot_chart(filtered_df, selected_features_df)