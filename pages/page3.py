from navigation import make_sidebar
import streamlit as st
from utils import *

make_sidebar()

st.write( """# 🕵️ Add a meal""")

r1col1,r1col2,r1col3,r1col4 = st.columns([3,4,2,3])
r2col1,r2col2 = st.columns([7,5])
r3col1,r3col2,r3col3,r3col4 = st.columns([3,3,3,3])

if not st.session_state.macros_per_food_df.empty:
    r1col1.text_input(label = 'Name of the meal',key = "meal_name_p3",max_chars = 50,help = 'Eg. Lentill soup')
    enter_food_p3 = r1col2.selectbox(label = 'Enter food item', options = st.session_state.macros_per_food_df['food_name'].sort_values(),key = 'enter_food_p3')
    unit = get_unit_p1(enter_food_p3)
    if unit == 'weight':
        r1col3.number_input(label = 'Weight in grams',key = "quantity_p3",min_value = 0.0,max_value = 1000.0,step = 5.0,format="%.2f")
    elif unit == 'quantity':
        r1col3.number_input(label = 'Quantity in unit',key = "quantity_p3",min_value = 0,max_value = 100,step = 1)
    elif unit == 'volume':
        r1col3.number_input(label = 'Quantity in ml',key = "quantity_p3",min_value = 0.0,max_value = 1000.0,step = 1.0,format="%.2f")
    else:
        pass
    r1col4.write("")
    r1col4.write("")
    add_ing_button_p3 = r1col4.button('Add ingredients', on_click = add_ing_p3)

    r2col1.header('Meal ingredients')
    if 'meal_df' not in st.session_state:
        st.session_state.meal_df = pd.DataFrame(columns=['food_name','serving', 'protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories'])
    st.session_state.meal_df = r2col1.data_editor(st.session_state.meal_df,num_rows='dynamic',disabled=('food_name','serving', 'protein', 'fat', 'carbohydrates', 'fibre', 'sugar', 'salt', 'calories'))
    # Calculate the sum of numerical columns
    totals_df = cal_macros_totals(st.session_state.meal_df, per_day = False)
    fig = gen_donut_chart(totals_df)
    r2col2.plotly_chart(fig, use_container_width=True)
    r3col2.number_input(label = 'Enter final weight (grams)',key = "meal_weight_p3",min_value = 1.0,max_value = 1500.0,step = 5.0,format="%.2f") 
    r3col3.write("")
    r3col3.write("")
    r3col3.button('Add this meal', on_click = add_meal_p3)
    
