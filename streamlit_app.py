# Import Python packages
import streamlit as st
import requests

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# ---------------------------------------------------------
# Page title
# ---------------------------------------------------------

st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    "Choose the fruits you want in your custom Smoothie!"
)


# ---------------------------------------------------------
# Get the current Snowflake session
# ---------------------------------------------------------

session = get_active_session()


# ---------------------------------------------------------
# Get the name of the smoothie
# ---------------------------------------------------------

name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# ---------------------------------------------------------
# Get fruit options from Snowflake
# ---------------------------------------------------------

my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)


# ---------------------------------------------------------
# Choose ingredients
# ---------------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# ---------------------------------------------------------
# Display selected ingredients
# ---------------------------------------------------------

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    st.write(
        "Your selected ingredients:",
        ingredients_string
    )


# ---------------------------------------------------------
# Submit smoothie order
# ---------------------------------------------------------

if name_on_order and ingredients_list:

    time_to_insert = st.button("Submit Order")

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


# ---------------------------------------------------------
# SmoothieFroot API
# ---------------------------------------------------------

st.subheader("🍉 SmoothieFroot Nutrition Information")


smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)


# Display the JSON response as a Python object
st.json(smoothiefroot_response.json())
