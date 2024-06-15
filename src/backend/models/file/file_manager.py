from dataclasses import dataclass
from enum import Enum
import pandas as pd
import polars as pl
from psycopg2 import errors
from sqlalchemy import exc


from common.all_enums import FILE_TYPE
from utils.logger import logger

@dataclass
class FileManager():
    file_io : bytes
    filename: str
    file_extension: str

    def read_file_in_chunks(self, engine_con, schema:str):
        logger.info(f'Detected file type : {self.file_extension}')
        logger.info(f'Con string : {engine_con}')
        try:
            match self.file_extension:
                
                    case FILE_TYPE.csv:
                        # csv_df = pl.read_csv(self.file_io)
                        # csv_df.write_database(table_name=self.filename,connection=engine_con,if_exists='append')
                        csv_df = pd.read_csv(self.file_io)
                        csv_df.to_sql(name=self.filename, con=engine_con,if_exists='replace',schema=schema, index=False)
                        logger.info(f'Columns found : {list(csv_df.columns)}')                        
                    
                    case FILE_TYPE.excel | FILE_TYPE.xls | FILE_TYPE.xlsx:
                        excel_df = pd.read_excel(self.file_io, sheet_name=None)
                        for sub_sheet in excel_df.keys():
                            excel_df.get(sub_sheet).to_sql(name=self.filename + '_' + str(sub_sheet), con=engine_con,if_exists='replace',schema=schema,index=False)
                            logger.info(f'Columns found : {list(excel_df.get(sub_sheet).columns)}')
                    
                    case FILE_TYPE.json:
                        json_df = pd.read_json(self.file_io).to_sql(name=self.filename, con=engine_con,if_exists='replace',index=False)
                    
                    case FILE_TYPE.xml:
                        xml_df = pd.read_xml(self.file_io).to_sql(name=self.filename, con=engine_con,if_exists='replace',index=False)
                    case _:
                        raise ValueError(f'Provided file type is not supported, please select one of {FILE_TYPE.list()}')
                 
            logger.info(f'Uploaded {self.filename} file succssfully..')

        except exc.OperationalError as e:
            logger.error("Valid connection details were not provided, failed connecting to db..", exc_info=1)
            raise ValueError("Valid connection details were not provided, failed connecting to database")