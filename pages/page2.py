from navigation import make_sidebar
import streamlit as st
from utils import *

make_sidebar()

st.write( """# 🕵️ Add food items""")

col1, col2, col3, col4= st.columns(4)
col1.selectbox(label = 'Category', 
                key="category_p2",
                options = ['Egg','Poultry','Meat','Seafood','Vegetable','Oils','Supplements','Spreads','Nuts','Pulses','Grains','Bread','Pasta','Dairy','Fruit','Pickles','Sugar','Beverages'],
                help = 'Eg. Spreads')
col2.text_input(label = 'Name of the food',key = "food_name_p2",max_chars = 80,help = 'Eg. Skippy peanut butter')
col3.text_input(label = 'Brand',key = "brand_name_p2",max_chars = 40,help = 'Eg. Skippy')
col4.selectbox(label = 'Unit',
               key = "unit_p2",
               options = ['Weight (100 grams)','Quantity (1 unit)', 'Volume (100 ml)'],
               help = 'If unit is "Weight", enter macros per 100 grams. If unit is "Quantity", enter macros per 1 quantity.')

col2, col3, col4, col5, col6, col7, col8  = st.columns(7)
col2.number_input(label = 'Protein',key = "protein_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f") 
col3.number_input(label = 'Fat',key = "fat_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f")
col4.number_input(label = 'Carbs',key = "carbs_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f")
col5.number_input(label = 'Sugar',key = "sugar_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f")
col6.number_input(label = 'Fibre',key = "fibre_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f")
col7.number_input(label = 'Salt',key = "salt_p2",min_value = 0.0,max_value = 100.0,step = 5.0,format="%.2f")
col8.number_input(label = 'Calories',key = "calories_p2",min_value = 0.0,max_value = 1000.0,step = 5.0,format="%.2f")
st.button('Add', on_click = add_food_p2)