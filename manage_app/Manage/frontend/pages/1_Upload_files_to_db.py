import json
from enum import Enum
from getpass import getpass

import requests
import streamlit as st

# from backend.common.all_enums import DBOptions


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class DBOptions(str, ExtendedEnum):
    Snowflake = "snowflake"
    Postgresql = "postgresql"


def upload_file_to_db_form():
    st.session_state.database = st.selectbox(
        "Database Client",
        index=None,
        options=DBOptions.list(),
        placeholder="postgresql",
    )
    hostname = st.text_input(label="Host/Server")
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    port = st.text_input(label="Port number", placeholder=1234, value=None)
    database_name = st.text_input(label="Database to use")
    files = st.file_uploader(
        label="Drop files to upload", accept_multiple_files=True
    )

    files_to_upload = [
        ("files", (file.name, file.read(), file.type)) for file in files
    ]

    upload = st.button("Upload")
    if upload and files:
        json_form = {
            "database": (None, st.session_state.database),
            "hostname": (None, hostname),
            "database_name": (None, database_name),
            "username": (None, username),
            "password": (None, password),
            "port": (None, int(port)),
        }

        with st.spinner("Uploading files.."):
            response = requests.post(
                "http://127.0.0.1:8000/upload_file",
                data=json_form,
                files=files_to_upload,
            )
        if response.ok:
            return st.toast("Files uploaded to database successfully!")
        return st.warning(
            f'Failed uploading files to database, due to "{response.text}"!'
        )
    elif not files and upload:
        st.warning("Select files to upload !")


upload_file_to_db_form()
