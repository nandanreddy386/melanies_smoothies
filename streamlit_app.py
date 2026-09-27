import streamlit as st
from snowflake.snowpark.functions import col


# ---------------------------------------------------------
# Connect to Snowflake
# ---------------------------------------------------------
conn = st.connection("snowflake")
session = conn.session()


# ---------------------------------------------------------
# App title
# ---------------------------------------------------------
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)


# ---------------------------------------------------------
# Get smoothie name
# ---------------------------------------------------------
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write(
        "The name on your Smoothie will be:",
        name_on_order
    )


# ---------------------------------------------------------
# Get fruit options from Snowflake
# ---------------------------------------------------------
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .to_pandas()
)

fruit_options = my_dataframe["FRUIT_NAME"].tolist()


# ---------------------------------------------------------
# Choose up to 5 ingredients
# ---------------------------------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)


# ---------------------------------------------------------
# Convert selected ingredients into one string
# ---------------------------------------------------------
ingredients_string = ""

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "


# ---------------------------------------------------------
# Submit order
# ---------------------------------------------------------
submitted = st.button("Submit Order")


if submitted:

    # Check that a name and at least one ingredient were entered
    if not name_on_order:
        st.warning("Please enter a name for your smoothie.")

    elif not ingredients_list:
        st.warning("Please choose at least one ingredient.")

    else:

        # Escape apostrophes so the SQL statement remains valid
        safe_name = name_on_order.replace("'", "''")
        safe_ingredients = ingredients_string.strip().replace("'", "''")

        # Insert the order into Snowflake
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders
            (ingredients, name_on_order)
            VALUES
            ('{safe_ingredients}', '{safe_name}')
        """

        try:
            session.sql(my_insert_stmt).collect()

            st.success(
                f"Your Smoothie is ordered, {name_on_order}!",
                icon="🥤"
            )

        except Exception as e:
            st.error("Something went wrong while placing your order.")
            st.write(e)
