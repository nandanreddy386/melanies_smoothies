# Import Python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    "Choose the fruits you want in your custom Smoothie!"
)


# Get the current Snowflake session
session = get_active_session()


# Get the name of the smoothie
name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Get the fruit options from Snowflake
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)


# Multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# Only continue if ingredients have been selected
if ingredients_list:

    # Create an empty string
    ingredients_string = ''

    # Convert the LIST into a STRING
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Display the selected ingredients
    st.write(ingredients_string)


    # Create the INSERT statement
    my_insert_stmt = """
        insert into smoothies.public.orders
        (ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')
    """


    # Submit Order button
    time_to_insert = st.button("Submit Order")


    # Insert the order into Snowflake
    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered, " + name_on_order + "!",
            icon="🥤"
        )