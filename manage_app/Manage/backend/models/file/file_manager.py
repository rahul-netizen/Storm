from dataclasses import dataclass
from enum import Enum

import pandas as pd
import polars as pl
from common.all_enums import FILE_TYPE
from psycopg2 import errors
from sqlalchemy import exc


@dataclass
class FileManager:
    file_io: bytes
    filename: str
    file_extension: str

    def read_file_in_chunks(self, engine_con):
        # print(self.file_io)
        print(self.file_extension, list(FILE_TYPE))
        try:
            match self.file_extension:
                case FILE_TYPE.csv:
                    csv_df = pl.read_csv(self.file_io)
                    print(engine_con)
                    csv_df.write_database(
                        table_name=self.filename,
                        connection=engine_con,
                        if_exists="append",
                    )
                    print(csv_df.columns)

                case _:
                    raise ValueError(
                        "Provided file type is not supported, please select"
                        f" one of {FILE_TYPE.list()}"
                    )

        except exc.OperationalError:
            raise ValueError(
                """Valid connection details were not provided, failed connecting to database"""
            )
