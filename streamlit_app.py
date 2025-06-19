# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your smoothies.
  """
)

name_on_order = st.text_input('Name on Smoothie:')
##st.write('The name on your smoothie will be :',name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
#st.write(pd_df)

ingredients_list = st.multiselect('Choose upto 5 ingredients'
                                  ,my_dataframe
                                 ,max_selections=5)


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for each_fruit in ingredients_list:
        if each_fruit is None:
            continue  # Skip this item if it's None
        ingredients_string += each_fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', each_fruit,' is ', search_on, '.')

        st.subheader(each_fruit + 'Nutritional Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order }', icon="✅")



#st.text(smoothiefroot_response.json())

