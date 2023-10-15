import json

import requests
import streamlit as st

# st.set_page_config(
#     page_title='M Services',
# )

# st.title('Manage App')
# # if __name__ =='__main__':

# Set the page title and icon
st.set_page_config(
    page_title="Storm",
    page_icon="🧨",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

# Add a title and a short description
st.title("Welcome to **Storm**")
st.write("One stop destination for some services.. *no humour intended*")

# Add some visuals or images
# st.image("/Users/rahulkumar/Newtuple/Manage/backend/static/images/fury-unleashed-dramatic-tornado-lightning-storm_950053-8987.png", caption="Beautiful Image", use_column_width=True,width=50   )


# Add a footer or any additional information
st.write("© 2023 Storm. All rights reserved.")
