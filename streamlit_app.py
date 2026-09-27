# Import Python packages
import streamlit as st
import requests

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Get the current Snowflake session
session = get_active_session()


# Page title
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    "Choose the fruits you want in your custom Smoothie!"
)


# Get the name of the smoothie
name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Get the fruit options from Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)


# Choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# Only continue if ingredients have been selected
if ingredients_list:

    ingredients_string = ""

    # Get nutrition information for each selected fruit
    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/"
            + fruit_chosen.lower()
        )

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )


    # Display selected ingredients
    st.write(
        "Your selected ingredients:",
        ingredients_string
    )


    # Submit order button
    time_to_insert = st.button("Submit Order")


    # Insert the order into Snowflake
    if time_to_insert:

        session.sql(
            """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (INGREDIENTS, NAME_ON_ORDER)
            SELECT ?, ?
            """,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(
            "Your Smoothie is ordered, " + name_on_order + "!",
            icon="🥤"
        )
