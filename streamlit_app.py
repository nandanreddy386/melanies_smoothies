# Import Python packages
import streamlit as st
import requests
import pandas as pd

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


# Get fruit options from Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(
        col("FRUIT_NAME"),
        col("SEARCH_ON")
    )
)


# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()


# Choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)


# Only continue if ingredients have been selected
if ingredients_list:

    ingredients_string = ""

    # Loop through selected fruits
    for fruit_chosen in ingredients_list:

        # Add fruit to order string
        ingredients_string += fruit_chosen + " "

        # Find the SEARCH_ON value for the selected fruit
        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        # Display the search value
        st.write(
            "The search value for",
            fruit_chosen,
            "is",
            search_on,
            "."
        )

        # Display nutrition heading
        st.subheader(
            fruit_chosen + " Nutrition Information"
        )

        # Call SmoothieFroot API using SEARCH_ON
        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/"
            + search_on.lower()
        )

        # Display API response
        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )


    # Submit order button
    time_to_insert = st.button("Submit Order")


    # Insert order into Snowflake
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
