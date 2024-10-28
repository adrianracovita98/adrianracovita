import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Define a password
PASSWORD = "7#Gz8!qW3r%Yl2&Sn9x$Kd@5V"

# Create a function to check the password
def check_password():
    st.session_state["password_correct"] = False
    entered_password = st.text_input("Enter Password:", type="password")
    if st.button("Submit"):
        if entered_password == PASSWORD:
            st.session_state["password_correct"] = True
        else:
            st.error("Incorrect password")

# Check if the password is correct
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    check_password()
else:
    st.write("Welcome to the app!")
    
    # Title of the app
    st.title('Disease Data Visualization')
    
    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load the data
        data = pd.read_csv(uploaded_file)
    
        # Ensure correct data types and handle errors
        numeric_columns = ['Age', 'Severity', 'Duration', 'Cost', 'Prevalence', 'Hospitalizations', 'Deaths', 'Latitude', 'Longitude', 'Year']
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
        # Display the first few rows of the dataset
        st.write("Data Preview:")
        st.write(data.head())
    
        # Display summary statistics
        st.write("Summary Statistics:")
        st.write(data.describe())
    
       # # Recheck the data types after conversion
        st.write("Data Types:")
        #st.write(data.dtypes)
    
        # Filter numeric columns for visualization selection
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
        if not numeric_columns:
            st.error("No numeric columns available for visualization.")
        else:
            # Interactive filtering and sorting
            st.sidebar.subheader("Filter and Sort Data")
            age_range = st.sidebar.slider("Select Age Range", int(data['Age'].min()), int(data['Age'].max()), (int(data['Age'].min()), int(data['Age'].max())))
            severity_range = st.sidebar.slider("Select Severity Range", int(data['Severity'].min()), int(data['Severity'].max()), (int(data['Severity'].min()), int(data['Severity'].max())))
            cost_range = st.sidebar.slider("Select Cost Range", int(data['Cost'].min()), int(data['Cost'].max()), (int(data['Cost'].min()), int(data['Cost'].max())))
            year_range = st.sidebar.slider("Select Year Range", int(data['Year'].min()), int(data['Year'].max()), (int(data['Year'].min()), int(data['Year'].max())))
            sort_column = st.sidebar.selectbox("Sort by", numeric_columns, key="sort_column")
            sort_order = st.sidebar.radio("Sort Order", ['Ascending', 'Descending'], key="sort_order")
    
            # Filter and sort the data
            filtered_data = data[(data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1]) &
                                (data['Severity'] >= severity_range[0]) & (data['Severity'] <= severity_range[1]) &
                                (data['Cost'] >= cost_range[0]) & (data['Cost'] <= cost_range[1]) &
                                (data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
            filtered_data = filtered_data.sort_values(by=sort_column, ascending=(sort_order == 'Ascending'))
    
            # Multi-select for filtering by County
            selected_counties = st.multiselect("Select Counties to include in the analysis", options=data['County'].unique(), default=data['County'].unique())
    
            # Filter data based on selected counties
            filtered_data = filtered_data[filtered_data['County'].isin(selected_counties)]
    
            # Interactive Map
            st.subheader("Geographical Distribution Map")
    
            # Ensure the necessary columns are present
            if 'Latitude' in filtered_data.columns and 'Longitude' in filtered_data.columns:
                # Allow user to select the year for the map
                selected_year = st.selectbox("Select Year", filtered_data['Year'].unique(), key="map_year")
                map_data = filtered_data[filtered_data['Year'] == selected_year]
    
                # Allow user to select the parameter to display on the heatmap
                map_parameter = st.selectbox("Select parameter to display on the map", ['Prevalence', 'Hospitalizations', 'Deaths'], key="map_parameter")
    
                fig = px.scatter_mapbox(
                    map_data,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name='County',
                    hover_data=['Prevalence', 'Hospitalizations', 'Deaths'],
                    color=map_parameter,
                    size='Hospitalizations',
                    color_continuous_scale=px.colors.cyclical.IceFire,
                    size_max=15,
                    zoom=5,
                    mapbox_style="carto-positron"
                )
                fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                st.plotly_chart(fig)
            else:
                st.error("Latitude and Longitude columns are required for the map visualization.")  
            
            # Select columns for visualization
            x_column = st.selectbox("Select X column for scatter plot", numeric_columns, key="x_column")
            y_column = st.selectbox("Select Y column for scatter plot", numeric_columns, key="y_column")
    
            # Allow user to select the year for the scatter plots
            selected_year = st.selectbox("Select Year", filtered_data['Year'].unique(), key="scatter_year")
            scatter_data = filtered_data[filtered_data['Year'] == selected_year]
    
            # Seaborn Visualization
            st.subheader("Scatter plot with regression line")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.regplot(x=x_column, y=y_column, data=scatter_data.dropna(subset=[x_column, y_column]), ax=ax)
            ax.set_title(f'Scatter plot of {x_column} vs {y_column} (Year {selected_year})')
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
    
            # Plotly Visualization
            st.subheader("Interactive scatter plot")
            fig = px.scatter(scatter_data.dropna(subset=[x_column, y_column]), x=x_column, y=y_column, color='County', title=f'Interactive Scatter plot of {x_column} vs {y_column} (Year {selected_year})')
            st.plotly_chart(fig)
            
            # Additional Visualizations
            st.subheader("Bar plot of Prevalence by County")
            fig = px.bar(filtered_data, x='County', y='Prevalence', title=f'Prevalence by County (Year {selected_year})')
            st.plotly_chart(fig)
        
            st.subheader("Bar plot of Hospitalizations by County")
            fig = px.bar(filtered_data, x='County', y='Hospitalizations', title=f'Hospitalizations by County (Year {selected_year})')
            st.plotly_chart(fig)
            
            st.subheader("Bar plot of Deaths by County")
            fig = px.bar(filtered_data, x='County', y='Deaths', title=f'Deaths by County (Year {selected_year})')
            st.plotly_chart(fig)
    
            # Box Plot
            st.subheader("Box Plot")
            column_box = st.selectbox("Select column for box plot", numeric_columns, key="box_column")
            fig = px.box(filtered_data, x='County', y=column_box, title=f'Box plot of {column_box} by County')
            st.plotly_chart(fig)
    
            # Trend Analysis (Line Plot)
            st.subheader("Trend Analysis")
            trend_column = st.selectbox("Select column for trend analysis", numeric_columns, key="trend_column")
            fig = px.line(filtered_data, x='Year', y=trend_column, color='County', title=f'Trend of {trend_column} with Year by County')
            st.plotly_chart(fig)
            
            # Collaborative Features
            st.sidebar.subheader("Collaboration")
            user_name = st.sidebar.text_input("Enter your name")
            if user_name:
                st.sidebar.write(f"Welcome, {user_name}!")
                with st.sidebar.expander("Leave a comment"):
                    comment = st.text_area("Your comment")
                    if st.button("Submit Comment"):
                        st.sidebar.write(f"{user_name} commented: {comment}")
    
            # Data Download
            st.subheader("Download Filtered Data")
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv',
            )
