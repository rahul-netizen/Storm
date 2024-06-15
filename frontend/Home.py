import streamlit as st
import requests
import json
import os
import pages
from datetime import datetime


# Set the page title and icon
st.set_page_config(
    page_title="Storm",
    page_icon="🧨",
    menu_items={
        'Report a bug': "mailto:rahul+manage_app@newtuple.com",
        'About': "The manage app, to make your life a bit easier."
    },
)
# Add a title and a short description
st.title("Welcome to **Storm**")
st.write("One stop destination for some services.. *no humour intended*")

# embed streamlit docs in a streamlit app
# Add some visuals or imagess
st.image("./static/tenor.gif", use_column_width=True,width=10)

# Add a footer or any additional information
st.write(f"©{datetime.today().year}  Storm. All rights reserved.")