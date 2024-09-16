import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Custom CSS for the title section and select boxes
st.markdown(
    """
    <style>
    .title-section {
        background-color: #545e64;
        font-size: 4rem;
        font-weight: bold;
        font-family: Arial, sans-serif;
        padding: 10px;
        border-radius: 10px;
        color: #ffffff;
    }
    .stSelectbox {
        font-size: 2rem;
        color: #31333F;
        padding: 5px;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
states = {
    'Delhi': 'All_delhi_forecasted.csv',
    'West Bengal': 'WB_Final_forecast_to_27.csv',
    'Karnataka': 'karnataka_forecast_UPto_27.csv',
    'Maharashtra': 'Maharashtra_Peak_Load.csv',
    'UP': 'UPforecast_upto_27.csv'
}

# Dictionary of states and their corresponding CSV files

# Add a title with custom CSS
st.markdown('<div class="title-section">Hydro Vision</div>', unsafe_allow_html=True)

# Create two columns for the selectboxes
col1, col2 = st.columns(2)

# Add a selectbox to choose the state in the first column
with col1:
    selected_state = st.selectbox("Select State", list(states.keys()), key="state_select")

# Load data based on the selected state
data = pd.read_csv(states[selected_state])
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df.set_index('Date', inplace=True)

# Extract years from the Date index
years = df.index.year.unique().tolist()
years.insert(0, "All Years")

# Add a selectbox to choose the year in the second column
with col2:
    selected_year = st.selectbox("Select Year", years, key="year_select")

# Filter the DataFrame based on the selected year
if selected_year == "All Years":
    filtered_df = df
else:
    filtered_df = df[df.index.year == selected_year]

# Create two columns for the table and the plot
col1, col2 = st.columns([10, 4])

# Display filtered DataFrame in the first column
with col2:
    st.write(filtered_df)

# Create Plotly figure with custom colors
fig = px.line(filtered_df, x=filtered_df.index, y=['Demand', 'Forecasted Demand'], title='Demand and Forecasted '
                                                                                              'Demand Over Time')
fig.update_traces(line=dict(color='red'), selector=dict(name='Demand'))
fig.update_traces(line=dict(color='blue'), selector=dict(name='Forecasted Demand'))

# Disable zoom and pan interactions
fig.update_layout(dragmode=False)
fig.update_layout(xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))

# Show the plot in the second column
with col1:
    st.plotly_chart(fig, use_container_width=True)