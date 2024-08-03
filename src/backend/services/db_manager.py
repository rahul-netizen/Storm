from dataclasses import dataclass
# from pydantic import BaseModel
import sqlalchemy as db
from sqlalchemy.engine import URL
# from snowflake.sqlalchemy import URL as snowflake_url
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine, inspect

# TODO: Move all enums to common dir
# from models.file.file_schema import DBOptions

from common.all_enums import DBOptions

# url =f'{use_db}://{user}:{password}@{host}:{port}/{db_name}'

@dataclass()
class Database():
    """Class for mainting the database connection information"""
    _username: str
    _password: str
    _hostname: str
    _port: int
    _database_name: str
    _schema: str #= "public"
    
    def get_connection_string(self) -> str :
        pass 

    def get_engine(self) -> db.engine:
        pass
    
    # class Config:
    #     orm_mode = True

@dataclass
class Postgres(Database):
    def get_connection_string(self) -> str:
        return URL.create(
            drivername='postgresql',
            username=self._username,
            password=self._password,
            host=self._hostname,
            port=self._port,
            database=self._database_name,
        )
    
    def get_engine(self, connection_string: str) -> db.engine:
        engine = create_engine(connection_string,pool_size=5, max_overflow=10, pool_pre_ping=True)   
        return engine     


@dataclass
class Snowflake(Database):
    def get_connection_string(self) -> str:
        def snowflake_url(**kwargs):
            pass
        return snowflake_url(
            # drivername='snowflake',
            account=self._hostname,
            user=self._username,
            password=self._password,
            # port=self._port,
            database=self._database_name,
        )
    def get_engine(self, connection_string: str) -> db.engine:
        engine = create_engine(connection_string,pool_size=5, max_overflow=10, pool_pre_ping=True)   
        return engine   
    
@dataclass
class Bigquery(Database):
    def get_connection_string(self) -> str:
        return f"bigquery://{self._database_name}"

    def get_engine(self, connection_string: str) -> db.engine:
            engine = create_engine(connection_string,pool_size=5, max_overflow=10, pool_pre_ping=True)   
            return engine 
@dataclass
class DBManager(Database):

    _db_client: str

    def get_db_client_by_name(self):
        match self._db_client:
            case DBOptions.Postgresql:
                connection_string = Postgres.get_connection_string(self)
                return Postgres(self._username,self._password,self._hostname,self._port,self._database_name,self._schema).get_engine(connection_string)
            case DBOptions.Snowflake:
                connection_string = Snowflake.get_connection_string(self)
                print(connection_string)
                return Snowflake(self._username, self._password, self._hostname, self._port, self._database_name, self._schema).get_engine(connection_string)
            case _:
                return f"{DBManager._db_client} not supported yet!"
            
    def get_connection_string(self) -> str:
        # return super().get_connection_string()
        match self._db_client:
            case DBOptions.Postgresql:
                return Postgres.get_connection_string(self)
            case DBOptions.Snowflake:
                return Snowflake.get_connection_string(self)
            case _:
                return f"{DBManager._db_client} not supported yet!"
    
    def get_db_schema(self) -> str:
        return self._schema