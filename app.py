import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Import-Export Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page background color and custom CSS
page_bg_color = """
    <style>
    body {
        background-color: #e8f5e9;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
    }
    .metric-box {
        padding: 15px;
        margin: 5px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #333333;
    }
    .metric-value {
        font-size: 20px;
        color: #007bff;
    }
    .metric-delta {
        color: #ff6b6b;
    }
    </style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title('📦 Import-Export Dashboard')

df= pd.read_csv(r'Imports_Exports_Dataset.csv')
my_sample=df.sample(n=3001, random_state=55040)

st.sidebar.title('Filters')
import_export_filter = st.sidebar.selectbox('Select Import or Export', ['Export', 'Import'], index=0)
top_n_countries = st.sidebar.slider('Top N Countries', min_value=5, max_value=20, value=10)
variable_selection = st.sidebar.selectbox('Select Variable for Distribution', ['Value', 'Quantity', 'Weight'])

# Assuming there's a 'Date' column in the dataset
# Modify this part to ensure the date is parsed correctly with day first

filtered_data = my_sample[my_sample['Import_Export'] == import_export_filter]

# If the Date column has the format "day-month-year", we can pass `dayfirst=True` to handle it.
if 'Date' in filtered_data.columns:
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], dayfirst=True, errors='coerce')

# Main Dashboard Title
#st.title('Interactive Imports and Exports Dashboard')

### 1. Top Countries Bar Plot
st.subheader(f'Top {top_n_countries} Countries by {import_export_filter} Volume')
top_countries = filtered_data.groupby('Country')['Quantity'].sum().nlargest(top_n_countries)

fig, ax = plt.subplots(figsize=(10, 6))
top_countries.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title(f'Top {top_n_countries} Countries by {import_export_filter} Volume')
ax.set_xlabel('Country')
ax.set_ylabel('Total Quantity')
ax.set_xticklabels(top_countries.index, rotation=45)
st.pyplot(fig)

### 2. Distribution Plot (Histogram)
st.subheader(f'Distribution of {variable_selection}')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data[variable_selection], bins=30, kde=True, ax=ax)
ax.set_title(f'Distribution of {variable_selection}')
ax.set_xlabel(variable_selection)
ax.set_ylabel('Frequency')
st.pyplot(fig)

### 3. Correlation Heatmap
st.subheader('Correlation Heatmap of Non-Categorical Variables')
# Selecting numerical columns for correlation
correlation_columns = ['Quantity', 'Value', 'Customs_Code', 'Weight', 'Invoice_Number']  # Adjust based on your dataset

# Correlation matrix
correlation_data = filtered_data[correlation_columns].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Heatmap')
st.pyplot(fig)

### 4. Export/Import Trends Over Time (Line Plot)
# Since there is a 'Date' column, we now process this correctly and filter data based on date
if 'Date' in filtered_data.columns:
    st.subheader(f'{import_export_filter} Trends Over Time')
    
    # Filtered data should now have correct Date parsing
    filtered_data.set_index('Date', inplace=True)
    
    # Aggregating data by date (daily, monthly, etc.)
    daily_data = filtered_data.resample('D')['Quantity'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    daily_data.plot(kind='line', marker='o', ax=ax)
    ax.set_title(f'{import_export_filter} Quantity Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Quantity')
    st.pyplot(fig)

### 5. Pie Chart for Country Share of Export/Import
st.subheader(f'Country Share of {import_export_filter} Volume')

# Pie chart for country distribution
fig, ax = plt.subplots(figsize=(8, 6))
top_countries.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, colors=sns.color_palette("Set3"))
ax.set_ylabel('')  # Hide y-axis label for pie chart
ax.set_title(f'{import_export_filter} Volume Share by Country')
st.pyplot(fig)

### 6. Summary Metrics
st.subheader('Key Summary Metrics')

# Calculating summary metrics
total_value = filtered_data['Value'].sum()
total_quantity = filtered_data['Quantity'].sum()
average_transaction_value = filtered_data['Value'].mean()

# Displaying metrics
col1, col2, col3 = st.columns(3)
col1.metric(label="Total Value", value=f"${total_value:,.2f}")
col2.metric(label="Total Quantity", value=f"{total_quantity:,.0f}")
col3.metric(label="Average Transaction Value", value=f"${average_transaction_value:,.2f}")
