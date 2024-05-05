import streamlit as st
from navigation import make_sidebar
from utils import *
from streamlit_timeline import st_timeline

make_sidebar()

st.write("""# 🔓 My Macros""")
r1col1,r1col2 = st.columns([5,7])
with st.sidebar:
    st.divider()
    st.write('Add your macros')
    if not st.session_state.macros_per_food_df.empty:
        meal_checked = st.checkbox("Add meal", key = 'meal_checked_p1')
        if meal_checked:
            options_df = st.session_state.meal_prep_df.sort_values(by = 'date_time', ascending = False)
            options = options_df['meal_name'] + '_' + options_df['date_time'].str[:10]
            enter_food_p1 = st.selectbox(label = 'Enter food', options = options,key = 'enter_food_p1')
            st.sidebar.number_input(label = 'Weight in grams',key = "quantity_p1",min_value = 0.0,max_value = 1000.0,step = 5.0,format="%.2f")
        else:
            options = st.session_state.macros_per_food_df['food_name'].sort_values()
            enter_food_p1 = st.selectbox(label = 'Enter food', options = options,key = 'enter_food_p1')
            unit = get_unit_p1(enter_food_p1)
            if unit == 'weight':
                st.sidebar.number_input(label = 'Weight in grams',key = "quantity_p1",min_value = 1.0,max_value = 1000.0,step = 5.0,format="%.2f")
            elif unit == 'quantity':
                st.sidebar.number_input(label = 'Quantity in unit',key = "quantity_p1",min_value = 1,max_value = 100,step = 1)
            elif unit == 'volume':
                st.sidebar.number_input(label = 'Quantity in ml',key = "quantity_p1",min_value = 1.0,max_value = 1000.0,step = 1.0,format="%.2f")
            else:
                pass
        col1, col2 = st.columns(2)
        col1.date_input('Date',value='today', key = 'date_p1', help ='Date of consumption')
        col2.time_input('Time', value="now", key = 'time_p1', help ='Time of consumption')
        st.sidebar.number_input(label = 'Meal number',key = "meal_num_p1",min_value = 1,max_value = 10,step = 1, help ='This is what meal of the day? Eg. if its the first meal, then its 1')
        st.button('Add', on_click = add_macros_p1)
        if st.session_state.food_added_p1 == 1:
            st.success('Food item successfully added!', icon='✅')
            st.session_state.food_added_p1 = 0
        elif st.session_state.food_added_p1 == 2:
            st.error('Enter quantity of the food item!', icon='🚨')
            st.session_state.food_added_p1 = 0
        else:
            pass
        st.page_link("pages/page2.py", label="Cannot find a food item:question:")
    else:
        st.page_link("pages/page2.py", label="Start adding food items")

# macros per day
totals_df = cal_macros_totals(st.session_state.macros_per_day_df, per_day = True)
fig_macros_per_day = gen_donut_chart(totals_df)
r1col1.plotly_chart(fig_macros_per_day,use_container_width=True)

# macros per meal
fig_macros_per_meal = gen_macros_per_meal_chart(st.session_state.macros_per_day_df)
r1col2.plotly_chart(fig_macros_per_meal,use_container_width=True)