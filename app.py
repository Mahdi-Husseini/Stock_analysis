import streamlit as st
import pandas as pd
import plotly.express as px
import re
import json
import yfinance as yf



data = pd.read_csv('C:\\Users\\user\\Desktop\\MSBA 350\\Lecture 1\\all_data_clean.csv')


file_path = "C:\\Users\\user\\Desktop\\MSBA 350\\Lecture 1\\data.json"

with open(file_path, "r", encoding="utf-8") as file:
    jdata = json.load(file)  # Use json.load() for files


st.title('Interactive Stock Price Analysis (2014-2024)')

st.header('MSBA 350 - Prof. Ghassan Chammas')

st.subheader('Group 1')

st.subheader('This is a simple web app that reads a CSV file of stocks from 2014-2024 and displays the data in a linechart.')

st.write('The data is from the Yahoo Finance API.')

st.dataframe(data, hide_index=True, column_config={'Date': st.column_config.Column(pinned=True)})

st.write('***')


# section description of each stocks and the names of it (like a presentation for each stock the user choose)

st.header('Tickers Description')

tick = st.selectbox('Ticker', options=list(jdata.keys())) # json


def extract_text(nested_list):
    while isinstance(nested_list, list):
        nested_list = nested_list[0]  # Keep unwrapping until it's a string
    return nested_list

description = extract_text(jdata[tick])

pattern = r"^[^.,]+"

match = re.search(pattern, description)

nom = match.group() if tick != 'CVS' else 'CVS Healthcare Corporation'

st.subheader(nom)


st.write(f'**Description:** {description}')

# Fetch the data for the ticker symbol
stock_data = yf.Ticker(tick)

hist = stock_data.history(period = '2d')

# Get the current close stock price
current_price = hist['Close'].iloc[-1]

previous_close = hist['Close'].iloc[-2]

# Calculate the price variation
price_variation = current_price - previous_close

# Update the delta value
delta = f'{price_variation:.2f}'

st.metric(label='Closing Price', value= f'${current_price:.2f}', delta = delta, border = True)

st.write('***')

# section stat of each stock (std, mean max, min)

st.header('Ticker Stats Across the 10 Years')

tick2 = st.selectbox('Ticker', options=list(jdata.keys()), key='market_indicator')

fmetrics = st.selectbox('Market Indicator', options=['Close', 'Open', 'High', 'Low', 'Volume'])

st.data_editor(data[f'{fmetrics}_{tick2}'].describe())

st.write('***')

# section the line graph

st.header('Lineplot of the Tickers Across the 10 Years')

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')


fmetrics = st.selectbox('Market Indicator', options=['Close', 'Open', 'High', 'Low', 'Volume'], key='viz')

viz_ticks = st.sidebar.multiselect('select ticker(s)', options=list(jdata.keys()), default= list(jdata.keys()))

start_date = st.sidebar.date_input(label='Start Date', value = '2014-01-02', min_value='2014-01-02', max_value='2024-12-30')
end_date = st.sidebar.date_input(label='End Date', value = '2024-12-30', min_value='2014-01-02', max_value='2024-12-30')

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

targets = []

for t in viz_ticks:
    targets.append(f'{fmetrics}_{t}')

fig = px.line(filtered, x='Date', y = targets)

title = f'{fmetrics} Prices' if fmetrics != 'Volume' else 'Volume of Shares'

fig.update_layout(title=f'{title} for Stocks')
fig.update_yaxes(title=title)

st.plotly_chart(fig)

st.info('''
    ##### before the stock price close for each day, blackrock was the highest

##### blackrock was volatile across the years 2018 -2022

##### there might be market insiders about the stock price affecting the fluctuation 

##### future predictions from prof in articles ( sentiment anlysis) are impcating investors decision buying or selling causing this market insiders shit

##### at the end of 2024 blackrock skyrocketed reaching 1000 per share making the gap huge
''')