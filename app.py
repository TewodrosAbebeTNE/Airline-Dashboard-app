import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image


st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .animated-title {
        font-size: 50px;
        text-align: center;
        color: #1f77b4;
        background-color: #e0f7fa;  /* Light blue background */
        padding: 10px;
        border-radius: 10px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    <h1 class='animated-title'>✈️ Airlines Flight Data Analysis 📊</h1>
    """,
    unsafe_allow_html=True
)
st.sidebar.title("Developer")
img = Image.open("te.jpg")
st.sidebar.image(img, caption="Tewodros A", use_container_width=True)
st.write("This app analyzes airlines flight data.")

try:
    df = pd.read_csv("airlines_flights_data.csv")
except FileNotFoundError:
    st.error("CSV file 'airlines_flights_data.csv' not found.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="
            background-color: #e3f2fd;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h3 style="color: #1976d2; margin: 0;">✈️ Flights</h3>
            <p style="font-size: 24px; font-weight: bold; color: #0d47a1; margin: 10px 0;">{len(df)}</p>
            <p style="color: #424242; margin: 0;">Total flights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="
            background-color: #e8f5e9;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h3 style="color: #388e3c; margin: 0;">🏢 Airlines</h3>
            <p style="font-size: 24px; font-weight: bold; color: #1b5e20; margin: 10px 0;">{df['airline'].nunique() if 'airline' in df.columns else 'N/A'}</p>
            <p style="color: #424242; margin: 0;">Unique airlines</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="
            background-color: #fff3e0;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 10px 0;
        ">
            <h3 style="color: #f57c00; margin: 0;">🌍 Destinations</h3>
            <p style="font-size: 24px; font-weight: bold; color: #e65100; margin: 10px 0;">{df['destination_city'].nunique() if 'destination_city' in df.columns else 'N/A'}</p>
            <p style="color: #424242; margin: 0;">Destination cities</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# for i, row in df.iterrows():
#     with st.expander(f"Flight {row['flight']}"):
#         st.write(f"Origin: {row['source_city']}")
#         st.write(f"Destination: {row['destination_city']}")
# Count the number of flights per airline
col4, col5, col6 = st.columns(3)
with col4:
    if 'airline' in df.columns:
        flight_counts = df['airline'].value_counts().reset_index()
        flight_counts.columns = ['Airline', 'Number of Flights']
        
        # Create interactive plot using Plotly
        fig = px.bar(flight_counts,
                     x='Airline', 
                     y='Number of Flights',
                     title='Flight Count by Airline',
                     color='Number of Flights',
                     color_continuous_scale='Blues',
                     text='Number of Flights')
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(xaxis_tickangle=-45,
                          height=500,
                          showlegend=False)
        
        # Display the interactive plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Column 'airline' not found in the data.")

with col5:
    if 'class' in df.columns and 'price' in df.columns:
        # Group by class and sum prices
        price_by_class = df.groupby('class')['price'].sum().reset_index()
        
        # Create interactive pie chart
        fig_pie = px.pie(price_by_class, 
                         values='price', 
                         names='class',
                         title='Total Revenue by Class',
                         color_discrete_map={'Economy': '#ff7f0e', 
                                           'Business': '#2ca02c', 
                                           'First': '#d62728'})
        
        fig_pie.update_traces(textposition='inside', 
                              textinfo='percent+label',
                              hovertemplate='<b>%{label}</b><br>Total: $%{value:,.0f}<br>Percentage: %{percent}')
        
        # Display the interactive pie chart in Streamlit
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Columns 'class' and/or 'price' not found in the data.")

with col6:
    if 'flight' in df.columns and 'duration' in df.columns:
        # Group by flight and sum durations
        duration_by_flight = df.groupby('flight')['duration'].sum().reset_index()
        
        # Create line chart showing flight vs total duration
        fig_line = px.line(
            duration_by_flight,
            x='flight',
            y='duration',
            title='Total Duration by Flight Number',
            markers=True,
            color_discrete_sequence=['#1f77b4']
        )
        
        fig_line.update_traces(
            mode='lines+markers',
            hovertemplate='<b>Flight %{x}</b><br>Total Duration: %{y} minutes<extra></extra>'
        )
        
        fig_line.update_layout(
            xaxis_title='Flight Number',
            yaxis_title='Total Duration (minutes)',
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        # Display the interactive line chart in Streamlit
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Columns 'flight' and/or 'duration' not found in the data.")
summary = df.groupby('airline')['price'].sum().reset_index()
col8, col9, col10 = st.columns(3)
with col8:
    with st.expander("Show the Summary Data", expanded=False):
        st.table(summary)
        
with col9:  # Indexing starts at 0, so column 9 is index 8
    csv = summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Summary",
        data=csv,
        file_name='airline_price_summary.csv',
        mime='text/csv'
    )
    

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 20px; margin-top: 40px;">
        <p style="color: #666; font-size: 14px;">
            ✈️ Airlines Flight Data Analysis Dashboard ✈️<br>
            By Tewodros A. Built with Python • Data updated daily • © 2025
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

