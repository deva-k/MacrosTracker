import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from streamlit_gsheets import GSheetsConnection
import json

def create_client_to_update():
    key_config = st.secrets['connections']['gsheets']
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    key_dict = {
                "type": key_config["type"],
                "project_id": key_config["project_id"],
                "private_key_id": key_config["private_key_id"],
                "private_key": key_config["private_key"],
                "client_email": key_config["client_email"],
                "client_id": key_config["client_id"],
                "auth_uri": key_config["auth_uri"],
                "token_uri": key_config["token_uri"],
                "auth_provider_x509_cert_url": key_config["auth_provider_x509_cert_url"],
                "client_x509_cert_url": key_config["client_x509_cert_url"],
                "universe_domain": key_config["universe_domain"],
                }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
    client = gspread.authorize(creds)
    return client

def get_unit_p1(enter_food_p1):
    if enter_food_p1:
        mpf_df = st.session_state.macros_per_food_df
        unit = mpf_df[mpf_df['food_name'] == enter_food_p1]['unit'].iloc[0]
    else:
        unit = 'Nothing is selected'
    return unit

def add_macros_p1():
    try:
        if st.session_state.quantity_p1 == 0:
            st.session_state.food_added_p1 = 2
        else:
            if st.session_state.meal_checked_p1:
                mpf_df = st.session_state.meal_prep_df
                meal_name = st.session_state.enter_food_p1.split('_')[0]
                macros_df = mpf_df[mpf_df['meal_name'] == meal_name][['weight', 'protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']]
                serving = macros_df['weight'].iloc[0] 
            else:
                mpf_df = st.session_state.macros_per_food_df
                macros_df = mpf_df[mpf_df['food_name'] == st.session_state.enter_food_p1][['serving', 'protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']]
                serving = macros_df['serving'].iloc[0] 
            macros_arr = np.array(macros_df[['protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']].iloc[0]) 
            macros_arr = (macros_arr * st.session_state.quantity_p1)/serving
            timestamp = datetime.datetime.combine(st.session_state.date_p1, st.session_state.time_p1)
            cs_obj = st.session_state.gsclient.open('Macros tracking').worksheet('macros_per_day')
            cs_obj.append_row([st.session_state.enter_food_p1,
                            json.dumps(timestamp,default = str).strip('"'),
                            st.session_state.quantity_p1,
                            macros_arr[0],
                            macros_arr[1],
                            macros_arr[2],
                            macros_arr[3],
                            macros_arr[4],
                            macros_arr[5],
                            macros_arr[6],
                            st.session_state.meal_num_p1,
                            st.session_state.user])
        st.session_state.food_added_p1 = 1
        st.session_state.quantity_p1 = 1
        st.session_state.meal_num_p1 = 1
        # update the meal per day df with the latest
        # read the sheet with users and passwords
        mpd_df = st.session_state.conn.read(worksheet="macros_per_day",ttl=0)
        # Drop rows where all values are NaN
        mpd_df = mpd_df.dropna(how='all')
        # Drop columns where all values are NaN
        mpd_df = mpd_df.dropna(how='all', axis = 1)
        st.session_state.macros_per_day_df = mpd_df[mpd_df['user_name'] == st.session_state.user].reset_index(drop = True)
    except Exception as e:
        print(e)
        st.toast('Unable to add food item!', icon='🚨')

def add_food_p2():
    macros_arr = np.array([st.session_state.protein_p2, st.session_state.fat_p2, st.session_state.carbs_p2, st.session_state.sugar_p2, st.session_state.fibre_p2, st.session_state.salt_p2])
    if not st.session_state.food_name_p2 or not st.session_state.brand_name_p2:
        st.toast('Name of the food or Brand cannot be empty!', icon='🚨')
    elif all(var == 0 for var in macros_arr):
        st.toast('All macros cannot be 0', icon='🚨')
    elif st.session_state.calories_p2 == 0:
        st.toast('Calories cannot be 0', icon='🚨')
    else:
        if 'grams' in st.session_state.unit_p2 or 'ml' in st.session_state.unit_p2:
            serving = 100
        else:
            serving = 1
        try:
            cs_obj = st.session_state.gsclient.open('Macros tracking').worksheet('macros_per_food')
            cs_obj.append_row([st.session_state.category_p2,
                                st.session_state.food_name_p2.rstrip(' ').lstrip(' '),
                                st.session_state.brand_name_p2.rstrip(' ').lstrip(' '),
                                st.session_state.unit_p2.split(' (')[0].lower(),
                                serving,
                                st.session_state.protein_p2,
                                st.session_state.fat_p2,
                                st.session_state.carbs_p2, 
                                st.session_state.sugar_p2, 
                                st.session_state.fibre_p2, 
                                st.session_state.salt_p2, 
                                st.session_state.calories_p2,
                                st.session_state.user,
                                json.dumps(datetime.datetime.now(),default = str).strip('"')])
            st.toast('Food item successfully added to our database!', icon='✅')
            st.session_state.food_name_p2 = ''
            st.session_state.brand_name_p2 = ''
            st.session_state.protein_p2 = 0
            st.session_state.fat_p2 = 0
            st.session_state.carbs_p2 = 0 
            st.session_state.sugar_p2 = 0 
            st.session_state.fibre_p2 = 0 
            st.session_state.salt_p2 = 0
            st.session_state.calories_p2 = 0
            df = st.session_state.conn.read(worksheet="macros_per_food", ttl = "5s")
            # Drop rows where all values are NaN
            df = df.dropna(how='all')
            # Drop columns where all values are NaN
            st.session_state.macros_per_food_df = df.dropna(how='all', axis = 1)
        except Exception as e:
            print(e)
            st.toast('Failed to add food item to our database!', icon='🚨')

def add_ing_p3():
    mpf_df = st.session_state.macros_per_food_df
    macros_df = mpf_df[mpf_df['food_name'] == st.session_state.enter_food_p3][['food_name','serving', 'protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']]
    serving = macros_df['serving'].iloc[0] 
    # Get the numerical columns
    numeric_columns = macros_df.select_dtypes(include=['number']).columns
    # Multiply the numerical columns by the scalar
    macros_df[numeric_columns] = (macros_df[numeric_columns] * st.session_state.quantity_p3)/serving
    st.session_state.meal_df = pd.concat([st.session_state.meal_df,macros_df], ignore_index=True)
    st.session_state.meal_df = st.session_state.meal_df.groupby('food_name').agg('sum').reset_index()

def gen_donut_chart(totals_df):
    try:
        # r2col2.header('Meal macros')
        fig = px.pie(totals_df, values=totals_df.iloc[0, :-1], names=totals_df.columns[:-1], title='', hole=0.4)
        # Add labels directly on the segments and position them outside the chart
        fig.update_traces(textinfo='value+label', textposition='outside')
        # Hide the legend
        fig.update_layout(title="Today's Macro Nutrients", showlegend=False,height=350, width=350)
        # Add a suffix to the numbers in the labels
        fig.update_traces(texttemplate='%{label}: %{value}g') 
        # Add a label for the total value
        fig.add_annotation(x=0.5, y=0.6, text="Calories",
                        font=dict(color="black", size=14), showarrow=False)
        # Add annotation for the total value in the center
        fig.add_annotation(x=0.5, y=0.50, text=str(np.round(totals_df['calories'].iloc[0],1)),
                        font=dict(color="black", size=20), showarrow=False)
    except:
        # Create an empty DataFrame with column names
        empty_df = pd.DataFrame(columns=['labels', 'values'])

        # Plot using Plotly Express
        fig = px.pie(empty_df, names='labels', values='values', 
                    title="Today's Macro Nutrients")
        # Hide the legend
        fig.update_layout(title="Today's Macro Nutrients", showlegend=False,height=350, width=350)
    return fig

def add_meal_p3():
    if not st.session_state.meal_name_p3:
        st.toast('Name of the meal cannot be empty!', icon='🚨')
    elif len(st.session_state.meal_df) < 2:
        st.toast('A meal must have more than a single ingredient!', icon='🚨')
    else:
        # Calculate the sum of numerical columns
        column_totals = st.session_state.meal_df[['protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']].sum()
        # Create a new DataFrame for the column totals
        totals_df = pd.DataFrame(column_totals).T
        cs_obj = st.session_state.gsclient.open('Macros tracking').worksheet('meal_prep')
        cs_obj.append_row([st.session_state.meal_name_p3.rstrip(' ').lstrip(' '),
                            st.session_state.meal_weight_p3,
                            totals_df.protein.iloc[0],
                            totals_df.fat.iloc[0],
                            totals_df.carbohydrates.iloc[0], 
                            totals_df.fibre.iloc[0], 
                            totals_df.sugar.iloc[0], 
                            totals_df.salt.iloc[0], 
                            totals_df.calories.iloc[0],
                            st.session_state.user,
                            json.dumps(datetime.datetime.now(),default = str).strip('"')])
        st.toast('Food item successfully added to our database!', icon='✅')


def cal_macros_totals(df, per_day = True):
    try:
        if per_day:
            # Calculate the sum of numerical columns
            column_totals = df[df['date_time'].str[:10] == str(datetime.date.today())][['protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']].sum()
        else:
            column_totals = df[['protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories']].sum()
        # Create a new DataFrame for the column totals
        totals_df = pd.DataFrame(column_totals).T
        totals_df.index = ['totals']
    except:
        totals_df = pd.DataFrame()
    return totals_df.round(2)

def gen_macros_per_meal_chart(df):
    try:
        df = df[df['date_time'].str[:10] == str(datetime.date.today())][['meal_number','protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt','calories']]
        # Group by Date and sum the nutrient columns
        df_grouped = df.groupby('meal_number').sum().reset_index()
        print(df_grouped)
        # Melt the dataframe to have 'Date' as x-axis, 'value' as y-axis, and 'variable' as color
        df_melted = df_grouped[['meal_number','protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt']].melt(id_vars=['meal_number'], var_name='Nutrient', value_name='Value')
        # Plot using Plotly Express
        fig_mac_per_meal = px.bar(df_melted, x='meal_number', y='Value', color='Nutrient', barmode='group',
                    title='Macro Nutrients per meal', labels={'meal_number': 'Meal number', 'Value': 'Total Amount', 'Nutrient': 'Nutrient Type'},height=350)
        # Restrict x-axis ticks to integers only
        fig_mac_per_meal.update_xaxes(tickvals=df_grouped['meal_number'].unique(), tickmode='array')

        # Add total calories on top of each group
        for i, row in df_grouped.iterrows():
            total_calories = row['calories']
            max_bar = max(row[['protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt']])
            fig_mac_per_meal.add_annotation(x=row['meal_number'], y=max_bar + 20, 
                            text=f"Total Calories: {total_calories}", 
                            showarrow=False, font=dict(size=12))
    except:
        # Create an empty DataFrame with column names
        empty_df = pd.DataFrame(columns=['x_axis', 'y_axis'])

        # Plot using Plotly Express
        fig_mac_per_meal = px.bar(empty_df, x='x_axis', y='y_axis', 
                    title='Macro Nutrients per meal',
                    labels={'x_axis': 'Meal number', 'y_axis': 'Total Amount'},
                    width=800)

    return fig_mac_per_meal


