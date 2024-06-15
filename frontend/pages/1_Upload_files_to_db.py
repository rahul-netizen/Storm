# import streamlit as st
import requests
import json
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
from os import environ
from enum import Enum
# from backend.common.all_enums import DBOptions
from Home import st
_ = load_dotenv(find_dotenv('.env.dev'))

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class DBOptions(str, ExtendedEnum):
    Snowflake = "snowflake"
    Postgresql = "postgresql"

def upload_file_to_db_form():
    st.warning("Snowflake adapter in maintenence, please try again later ⚠️!")
    st.session_state.database = st.selectbox('Database Client',index=None, options= DBOptions.list(),placeholder='Select database')
    hostname = st.text_input(label='Host/Server/Account')
    username = st.text_input(label='Username')
    password = st.text_input(label="Password", type="password")
    port = 5432
    if not st.session_state.database == DBOptions.Snowflake:
        port = st.text_input(label="Port number",placeholder='5432 be default',value=5432)
    database_name = st.text_input(label="Database to use")
    schema = st.text_input(label="Schema to use",placeholder="Select schema, public by default")
    files = st.file_uploader(label="Drop files to upload",accept_multiple_files=True)
    json_file = st.file_uploader(label="Drop json file")
    files_to_upload = [("files",(file.name, file.read(), file.type)) for file in files]
    
    upload = st.button('Upload')
    if upload and files:
        if json_file:
            files_to_upload.append(("json_file", (json_file.name, json_file.read(), json_file.type)))
        json_form = {
            "database" : (None,st.session_state.database),
            "hostname" : (None,hostname),
            "database_name" : (None,database_name),
            "username" : (None,username),
            "password" : (None,password),
            "port" : (None,int(port)),
            "schema" : (None,schema),
        }

        with st.spinner("Uploading files.."):
            api_url = environ.get("BACKEND_HOST") + ':' + environ.get("BACKEND_PORT")
            response = requests.post(api_url + '/upload_file', data=json_form,files=files_to_upload)
        if response.ok:
            return st.toast('Files uploaded to database successfully!')
        return st.warning(f'Failed uploading files to database, due to "{response.text}"!')
    elif not files and upload :
        st.warning('Select files to upload !')


def authenticate():
    import streamlit_authenticator as stauth
    import yaml
    from yaml.loader import SafeLoader

    with open('/Users/rahulkumar/Newtuple/Manage/frontend/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    authenticator.login('main')

    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'sidebar', key='unique_key')
        st.info(f'Welcome *{st.session_state["name"]}*')
        upload_file_to_db_form()

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # generate new hash & save in config
    # import streamlit_authenticator as stauth
    # stauth.Hasher(['abc']).generate()
    # ['$2b$12$daJP6x60a0z7ItGXVtybHO8Dh7VYg//wUouZBYYLd5P57cl1BR182']

if __name__ == "__main__":
    authenticate()