import streamlit as st
import pandas as pd
import numpy as np


# Function to load the data
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    
    # Convert 'Fecha_De_Registro' to datetime, while handling 'am'/'pm'
    df['Fecha_De_Registro'] = pd.to_datetime(df['Fecha_De_Registro'], format='%d/%m/%Y %I:%M%p')
    
    df['day'] = df['Fecha_De_Registro'].dt.date
    df['week'] = df['Fecha_De_Registro'].dt.isocalendar().week
    df['month'] = df['Fecha_De_Registro'].dt.month
    return df

# File uploader in a container at the beginning of the app
with st.container():
    st.title("Upload your data")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Container for "Estadística Descriptiva"
    with st.container():
        st.title("Estadística Descriptiva")
        
        # Calculate the total, average, last week's average, and last month's average for each company
        companies = df['Razon_Social_Empresa'].unique()
        data = []
        for company in companies:
            company_df = df[df['Razon_Social_Empresa'] == company]
            total = company_df['Crypto transferido por empresa'].sum()
            average = company_df['Crypto transferido por empresa'].mean()
            last_week_average = company_df[company_df['week'] == df['week'].max()]['Crypto transferido por empresa'].mean()
            last_month_average = company_df[company_df['month'] == df['month'].max()]['Crypto transferido por empresa'].mean()
            num_transactions = len(company_df)
            data.append([company, total, average, last_week_average, last_month_average, num_transactions])
        
        # Create a DataFrame from the data
        summary_df = pd.DataFrame(data, columns=['Razon_Social_Empresa', 'Total Crypto transferido por empresa', 'Promedio Crypto transferido por transacción', 'Promedio de la última semana', 'Promedio del último mes', 'Número Total de Transacciones'])
        
        # Format numerical columns as string with 2 decimal places
        for column in ['Total Crypto transferido por empresa', 'Promedio Crypto transferido por transacción', 'Promedio de la última semana', 'Promedio del último mes']:
            summary_df[column] = summary_df[column].apply(lambda x: '{:,.2f}'.format(x) if pd.api.types.is_number(x) else x)
        
        st.table(summary_df)


    # Container for "Estadísticas por período seleccionado"
    with st.container():
        st.title("Estadísticas por período seleccionado")
        
        # Date input for the user to select a time range
        start_date, end_date = st.date_input("Select a date range", [df['Fecha_De_Registro'].min().date(), df['Fecha_De_Registro'].max().date()])
        
        # Filter the dataframe based on the selected dates
        filtered_df = df[(df['Fecha_De_Registro'].dt.date >= start_date) & (df['Fecha_De_Registro'].dt.date <= end_date)]
        
        # Calculate the total, average, last week's average, and last month's average for each company
        companies = filtered_df['Razon_Social_Empresa'].unique()
        data = []
        for company in companies:
            company_df = filtered_df[filtered_df['Razon_Social_Empresa'] == company]
            total = company_df['Crypto transferido por empresa'].sum()
            average = company_df['Crypto transferido por empresa'].mean()
            num_transactions = len(company_df)
            data.append([company, total, average, num_transactions])
        
        # Create a DataFrame from the data
        summary_df = pd.DataFrame(data, columns=['Razon_Social_Empresa', 'Total Crypto transferido por empresa', 'Promedio Crypto transferido por transacción', 'Número Total de Transacciones'])
        
        # Format numerical columns as string with 2 decimal places
        for column in ['Total Crypto transferido por empresa', 'Promedio Crypto transferido por transacción']:
            summary_df[column] = summary_df[column].apply(lambda x: '{:,.2f}'.format(x) if pd.api.types.is_number(x) else x)
        
        st.table(summary_df)

#streamlit run app.py