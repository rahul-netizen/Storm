from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class DBOptions(str, ExtendedEnum):
    Snowflake = "snowflake"
    Postgresql = "postgresql"


class FILE_TYPE(str, ExtendedEnum):
    csv: str = 'csv'
    excel: str = "excel"
